"""Fail if git-tracked files or any commit in history look like they hold a credential (`python3 scripts/no_secrets.py`)."""
import re
import subprocess
import sys

PATTERNS = re.compile(
    r"(sk-(?:proj-)?[A-Za-z0-9_-]{20,}|xai-[A-Za-z0-9]{20,}|tm_agent_[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}"
    r"|xox[abprs]-[A-Za-z0-9-]{10,}|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{35}|-----BEGIN [A-Z ]*PRIVATE KEY-----|\b\d{8,10}:AA[A-Za-z0-9_-]{30,})")
ENV_LINE = re.compile(r"^\+?\s*([A-Z0-9_]*(?:KEY|TOKEN|SECRET|PASSWORD|SID))\s*[=:]\s*[\"']?([A-Za-z0-9_\-/+.=]{12,})[\"']?\s*$")
KNOWN_FAKE = {"sk-abcdefghijklmnopqrstuvwxyz123456"}  # fixture in tests/test_systems.py
FAKE = re.compile(r"(fake|example|changeme|change-me|not-a-secret|test|dummy|demo|xxx|thirdmind|<|\$\{)", re.I)


def git(*a):
    return subprocess.run(["git", *a], capture_output=True, text=True, check=True).stdout


def scan(lines, where):
    bad = []
    for n, line in enumerate(lines, 1):
        if "no-secrets: allow" in line or any(k in line for k in KNOWN_FAKE):
            continue
        m = PATTERNS.search(line)
        e = ENV_LINE.match(line)
        if m or (e and not FAKE.search(e.group(2))):
            bad.append(f"{where}:{n}: {(m.group(0) if m else e.group(1) + '=')[:7]}…")
    return bad


def main():
    files = git("ls-files").split()
    bad = [f"{f}: env file is tracked" for f in files if re.search(r"(^|/)\.env(\.|$)", f) and not f.endswith(".env.example")]
    for f in files:
        try:
            bad += scan(open(f, encoding="utf-8").read().splitlines(), f)
        except (UnicodeDecodeError, FileNotFoundError):
            pass
    commits = git("rev-list", "--all").split()
    for c in commits:
        added = [line for line in git("show", "--format=", "--unified=0", c).splitlines() if line.startswith("+") and not line.startswith("+++")]
        bad += scan(added, f"commit {c[:8]}")
    for b in sorted(set(bad)):
        print("SECRET?", b)
    print(f"no-secrets: {len(files)} tracked files, {len(commits)} commits, {len(set(bad))} findings -> {'FAIL' if bad else 'PASS'}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
