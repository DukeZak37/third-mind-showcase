"""Fail if a relative link or image in a tracked Markdown/HTML file points at a missing file (`python3 scripts/check_links.py`)."""
import pathlib
import re
import subprocess
import sys

LINK = re.compile(r"""(?:\]\(|src=["']|href=["'])([^)"'#\s]+)""")

bad = []
files = subprocess.run(["git", "ls-files", "*.md", "*.html"], capture_output=True, text=True, check=True).stdout.split()
for f in files:
    for target in LINK.findall(pathlib.Path(f).read_text(encoding="utf-8")):
        if re.match(r"^[a-z]+:", target):
            continue
        if not (pathlib.Path(f).parent / target).exists():
            bad.append(f"{f}: {target}")
for b in bad:
    print("MISSING", b)
print(f"links: {len(files)} files, {len(bad)} missing -> {'FAIL' if bad else 'PASS'}")
sys.exit(1 if bad else 0)
