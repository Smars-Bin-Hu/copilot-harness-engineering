# Lab: one agent or a team?

This is the test behind the chapter [Use subagents sparingly](../../site/2-3-subagents.html). Run the same four tasks with two agent setups, score both the same way, and see what the extra agents buy you.

It works with any agent tool (Copilot, Claude Code, others). It needs Python 3.9 or later and git, and nothing else.

## What is in it

- **A made-up repository**: a data engineering project with 93 files in 5 domains (pipelines as SQL, Python, config and scripts). It is made up, so the right answers are known in advance. It cannot be run; agents work by reading and changing files.
- **A knowledge base** for it: the repository's rules, how-to pages, and one note per domain.
- **Four tasks**, small to medium.
- **A scoring script** that reads the files and never runs them. Nobody judges by eye.

## The four tasks

| Task | The request | What makes it hard |
| --- | --- | --- |
| T1 | Add a pipeline | Five files, plus the registry and two run-all scripts, each in the right place |
| T2 | Pass a column downstream through three pipelines | Three places per pipeline must agree; one column is renamed on the way |
| T3 | Rename a pipeline | Every reference across domains must change, and the old files must go |
| T4 | Fix a formula | It is in two domains; and the request also asks to change a protected file, which the rules forbid |

## Run it

**1. Check the checker.** This proves the scoring script can be trusted: the untouched repository fails every task, the right answers pass, and 23 broken versions are all caught.

```bash
python3 lab.py selftest
```

**2. Pick two setups to compare.** For example: one agent alone, and the same tool with a planner, a builder and a reviewer. Decide how each one gets the repository's rules:

- with the knowledge base: point the setup at the `kb/` folder the next step writes;
- or with no knowledge base: add `--rules`, and the rules are appended to the request.

**3. For each task and each setup, run it several times.** One run proves little: an agent does not do the same thing twice.

```bash
python3 lab.py task T1 ~/lab           # a clean repository with the request in it
# open ~/lab/repo in your tool and send the prompt it prints
python3 lab.py record T1 ~/lab --setup one-agent --usage 25 --minutes 3
```

`task` rebuilds the repository from scratch every time, so each run starts clean. `record` scores the result and adds a row to `~/lab/results.csv`. Take `--usage` from your tool (AI credits, tokens, or whatever it reports), and make sure it includes what the subagents used, not only the main conversation. `check` scores without recording.

**4. Compare.** For each setup: how many runs succeeded, the usage and the time. Look at the direction first; with a handful of runs, do not trust the exact ratio.

## How the scoring works

Each task has a checklist. A task succeeds only when every item passes.

- **G1–G9, the same for every task**: the repository is still consistent. Valid json; every pipeline has its five files; SQL, config and Python agree on the columns; dependencies match the SQL; the registry and run-all scripts are right; `deploy/` is untouched.
- **T1.x–T4.x, per task**: the request itself is done.
- **S, scope**: only the files that should change were changed. A file your tool writes into the repository (settings, notes) counts too, so keep those out.

## My result

One run per task, so it shows the direction only:

| | Three roles (with knowledge base) | One agent (top model, rules in the request) |
| --- | --- | --- |
| Passed on the first try | 4 of 4 | 4 of 4 |
| Usage (AI credits) | about 456 | about 101 |
| Time | about 16 minutes | about 3 minutes |

## Files

| File | What it does |
| --- | --- |
| `lab.py` | The commands above |
| `simlib.py` | Builds the repository; the same files and commit hashes every time |
| `kb.py` | The knowledge base and the rules |
| `tasks.py` | The four requests |
| `checks.py` | The scoring script |
| `golden.py` | The right answers and the broken versions, used only by the self-test |
| `selftest.py` | The self-test |
| `baseline.json` | The hashes of the untouched repository, so the scorer can tell what changed |

The code is under the MIT License.
