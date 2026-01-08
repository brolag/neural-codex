---
description: Cancel a running Ralph loop
argument-hint: none
---

Cancel an active Ralph loop.

Steps:
1) Check whether a `scripts/ralph-loop.sh` process is running (use `pgrep -f ralph-loop.sh`).
2) If running in the current terminal, advise `Ctrl-C`.
3) If running elsewhere, stop it with `kill <pid>`.
4) Verify the lock file `/tmp/ralph-loop.lock` is released; only remove it if no process is running.
5) Report the action taken and current loop status.
