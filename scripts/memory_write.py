#!/usr/bin/env python3
import argparse
import json
from datetime import datetime
from pathlib import Path


def utc_ts():
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def main():
    parser = argparse.ArgumentParser(description="Append a memory entry to plans/progress.jsonl")
    parser.add_argument("message", nargs="+", help="Memory note content")
    parser.add_argument("--status", default="note", help="note|preference|pattern|learning|forget")
    parser.add_argument("--task", default="memory", help="Task label for progress log")
    parser.add_argument("--progress", default="plans/progress.jsonl", help="Path to progress log")
    args = parser.parse_args()

    message = " ".join(args.message).strip()
    if not message:
        raise SystemExit("Message required")

    entry = {
        "ts": utc_ts(),
        "iteration": 0,
        "task": args.task,
        "status": args.status,
        "message": message,
    }

    progress_path = Path(args.progress)
    progress_path.parent.mkdir(parents=True, exist_ok=True)
    with progress_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=True))
        f.write("\n")

    print(f"Wrote memory entry to {progress_path}")


if __name__ == "__main__":
    main()
