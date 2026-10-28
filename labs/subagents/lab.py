"""Compare agent setups on four data engineering tasks. Standard library only.

    python3 lab.py task T1 <work folder> [--rules]   a clean repository with the request in it
    python3 lab.py check T1 <work folder> [--json]   score the result
    python3 lab.py record T1 <work folder> --setup NAME --usage N --minutes N
                                                    score it and add a row to <work folder>/results.csv
    python3 lab.py selftest                          prove the scoring script can be trusted

The work folder holds repo/ (the made-up repository), kb/ (its knowledge base) and results.csv.
"""
import argparse
import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import checks
import kb
import simlib
import tasks

HERE = Path(__file__).resolve().parent


def paths(work: str):
    root = Path(work).expanduser().resolve()
    return root, root / "repo", root / "kb"


def cmd_task(args) -> None:
    root, repo, kb_dir = paths(args.work)
    simlib.build_repo(repo)
    simlib.remove_tree(kb_dir)
    simlib.write_tree(kb_dir, kb.kb_files())
    (repo / "REQUIREMENT.md").write_text(tasks.requirement(args.task, rules=args.rules), encoding="utf-8")
    print(f"Repository: {repo}")
    print(f"Request:    {repo / 'REQUIREMENT.md'}" + ("  (the repository's rules are appended)" if args.rules else ""))
    if not args.rules:
        print(f"Knowledge base: {kb_dir}  (point your setup at it, or run with --rules instead)")
    print(f"\nOpen the repository in your tool and send:\n\n    {tasks.PROMPT}\n")
    print(f"When it is done: python3 {Path(__file__).name} check {args.task} {args.work}")


def score(args):
    _, repo, _ = paths(args.work)
    if not repo.is_dir():
        sys.exit(f"No repository at {repo}. Run: python3 lab.py task {args.task} {args.work}")
    return checks.check(args.task, repo)


def cmd_check(args) -> None:
    result = score(args)
    if args.json:
        print(json.dumps(result, indent=1))
        return
    for entry in result["items"]:
        print(("[pass] " if entry["ok"] else "[FAIL] ") + entry["id"] + " " + entry["text"]
              + (f"  <- {entry['detail']}" if entry["detail"] else ""))
    print(f"Score {result['score']}% ({result['passed']}/{result['total']}): "
          + ("SUCCESS" if result["success"] else "not passed"))


def cmd_record(args) -> None:
    result = score(args)
    root, _, _ = paths(args.work)
    out = root / "results.csv"
    new = not out.exists()
    with open(out, "a", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        if new:
            writer.writerow(["time", "task", "setup", "success", "passed", "total", "usage", "minutes"])
        writer.writerow([datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), args.task, args.setup,
                         result["success"], result["passed"], result["total"], args.usage, args.minutes])
    print(f"{args.task} {args.setup}: {result['passed']}/{result['total']}, "
          f"{'SUCCESS' if result['success'] else 'not passed'}. Added to {out}")


def cmd_selftest(_args) -> None:
    import runpy
    runpy.run_path(str(HERE / "selftest.py"), run_name="__main__")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    task = sub.add_parser("task", help="a clean repository with the request in it")
    task.add_argument("task", choices=sorted(tasks.REQUIREMENTS))
    task.add_argument("work")
    task.add_argument("--rules", action="store_true", help="append the repository's rules to the request")
    task.set_defaults(function=cmd_task)
    check = sub.add_parser("check", help="score the result")
    check.add_argument("task", choices=sorted(tasks.REQUIREMENTS))
    check.add_argument("work")
    check.add_argument("--json", action="store_true")
    check.set_defaults(function=cmd_check)
    record = sub.add_parser("record", help="score the result and add a row to results.csv")
    record.add_argument("task", choices=sorted(tasks.REQUIREMENTS))
    record.add_argument("work")
    record.add_argument("--setup", required=True, help="a short name, e.g. one-agent or three-roles")
    record.add_argument("--usage", required=True, help="what your tool reports, e.g. AI credits or tokens")
    record.add_argument("--minutes", required=True, type=float)
    record.set_defaults(function=cmd_record)
    sub.add_parser("selftest", help="prove the scoring script can be trusted").set_defaults(function=cmd_selftest)
    args = parser.parse_args()
    args.function(args)


if __name__ == "__main__":
    main()
