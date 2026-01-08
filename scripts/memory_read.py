#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Search plans/progress.jsonl for memory entries")
    parser.add_argument("query", nargs="*", help="Search query")
    parser.add_argument("--progress", default="plans/progress.jsonl", help="Path to progress log")
    parser.add_argument("--limit", type=int, default=10, help="Max results")
    args = parser.parse_args()

    query = " ".join(args.query).strip().lower()
    progress_path = Path(args.progress)
    if not progress_path.exists():
        print("No progress log found")
        return

    results = []
    with progress_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            haystack = " ".join(
                str(entry.get(key, ""))
                for key in ("task", "status", "message")
            ).lower()
            if not query or query in haystack:
                results.append(entry)

    if not results:
        print("No matching entries")
        return

    for entry in results[: args.limit]:
        ts = entry.get("ts", "")
        task = entry.get("task", "")
        status = entry.get("status", "")
        message = entry.get("message", "")
        print(f"[{ts}] ({task}/{status}) {message}")


if __name__ == "__main__":
    main()
