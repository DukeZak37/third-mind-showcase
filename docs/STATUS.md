# Real vs simulated: feature status

Labels used everywhere in this repo:

- **REPORTED LIVE**: running against a real service, as reported by the Devin build sessions with API responses.
- **DEV-TESTED**: automated tests pass on a development machine; not deployed.
- **SIMULATED**: mocked output, labeled as such wherever it appears.
- **PLANNED**: designed or discussed, not built.

Status as of 2026-11-20.

| Feature | Label | Notes |
|---|---|---|
| Skynet, a disclosed Discord bot in Duke's community server | REPORTED LIVE | Slash commands, button dashboards, role menu, 12 custom emoji, branded channel headers |
| Self-select interest roles (5) | REPORTED LIVE | Grant no permissions; opt-in only |
| `/status` and `/recall` in Discord | REPORTED LIVE | Read the real hub; memory contents stay private |
| A real person clicking the Discord buttons | **NOT YET VERIFIED** | A bot can't press its own buttons; automated tests simulate the click |
| Telegram community bot (admin in Duke's group, join welcome) | REPORTED LIVE | Disclosed bot; welcome message only, no auto-posting |
| Third Mind hub: agent registry, tasks, shared memory (PostgreSQL + pgvector), approvals, budgets, audit log, dashboard | DEV-TESTED | 78 tests rerun independently; 84 reported on the latest build |
| Guardian Forge: read-only security baseline (inventory, health, detections, dry-run alerts) | DEV-TESTED | Defensive and read-only: no blocking, scanning or credential handling |
| Evidence desk: operator review of agent actions and evidence | DEV-TESTED | Synthetic inputs only |
| GPT, Grok and Bahamut replies inside Discord | SIMULATED | Every reply is labeled SIMULATED until provider keys are approved |
| Twitch, Kick, X bookmarks, SMS reply codes, OBS overlay, content loop | SIMULATED | Built and tested in mock mode; no live accounts connected |
| Dedicated Grok Slack bot | PLANNED | The team uses a human-relayed workflow, not a dedicated Slack identity |
| Paper-trading bridge | PLANNED | Offline contracts only; no exchange access, no real orders |
| Current hub production rollout | NOT YET VERIFIED | The public evidence does not establish which hub revision or opt-in features are running |

What this repo is **not**: the implementation. The hub and connector code stay in private repos until they pass a
security and privacy review.
