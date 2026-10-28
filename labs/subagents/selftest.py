"""Can the scoring script be trusted? The untouched repository fails every task, the right answers pass, and every broken version is caught."""
import shutil
import sys
import tempfile
from pathlib import Path

import checks
import golden
import simlib

base = Path(tempfile.mkdtemp()) / "base"
simlib.build_repo(base)
simlib.write_baseline(base)
bad = 0


def fresh() -> Path:
    target = base.parent / "work"
    simlib.remove_tree(target)
    shutil.copytree(base, target)
    return target


for task in checks.TASKS:
    result = checks.check(task, base)
    failed = [i["id"] for i in result["items"] if not i["ok"]]
    ok = not result["success"] and all(i["ok"] for i in result["items"] if i["id"].startswith("G"))
    print(("OK  " if ok else "BAD ") + f"{task} untouched: global items pass, task items fail {failed}")
    bad += not ok
    work = fresh()
    golden.GOLDEN[task](work)
    result = checks.check(task, work)
    ok = result["success"]
    print(("OK  " if ok else "BAD ") + f"{task} right answer: {result['passed']}/{result['total']}" + ("" if ok else " failed: " + str([(i["id"], i["detail"]) for i in result["items"] if not i["ok"]])))
    bad += not ok
for task, name, expected, function in golden.MUTANTS:
    work = fresh()
    function(work)
    result = checks.check(task, work)
    failed = sorted(i["id"] for i in result["items"] if not i["ok"])
    ok = (not result["success"]) and all(item in failed for item in expected)
    print(("OK  " if ok else "BAD ") + f"{task} broken '{name}': failed {failed}, should include {expected}")
    bad += not ok
print("all good" if not bad else f"{bad} problem(s)")
sys.exit(1 if bad else 0)
