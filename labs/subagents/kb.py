"""The made-up knowledge base: the repository's rules (with --rules they go into the request instead),
one note per domain, and an index page."""
from typing import Dict

import simlib

RULES: Dict[str, str] = {}

RULES["rules/naming.md"] = """# Naming

- Names are lower case with underscores: `<domain>_<layer>_<table>`. Example: `customer_dw_profile`.
- The only domains are customer, account, txn, risk and product. The only layers are stg, dw and mart.
- Each pipeline has 5 files with the same name, in its own domain's folder:
  - `<domain>/sql/<name>.sql`
  - `<domain>/python/<name>.py`
  - `<domain>/config/<name>.json`
  - `<domain>/scripts/run_<name>.sh`
  - `<domain>/scripts/run_<name>.ps1`
- Target table: the schema is `<domain>_<layer>` and the table name is `<table>`. Example: `customer_dw.profile`.
- Table names are lower case with underscores, and never an SQL reserved word (for example limit, order, group).
- Source system tables are written `src_core.<table>`. Only the stg layer may read source system tables directly.
"""

RULES["rules/sql.md"] = """# SQL

- Every file starts with the same 3 comment lines, in this order:
  - `-- pipeline: <pipeline name>`
  - `-- layer: <layer>`
  - `-- owner: de-<domain>`
- One statement per file: `INSERT INTO <schema>.<table>`, then `SELECT` on the next line.
- One column per line in the SELECT, indented 4 spaces, comma at the end of the line, no comma after the last column.
- A column with an expression is written `<expression> AS <column name>`.
- SQL keywords in upper case. The statement ends with a semicolon.
- A new column goes at the end of the SELECT list.
- A table in FROM or JOIN must be `src_core.*` or the target table of another pipeline.
"""

RULES["rules/config.md"] = """# Config files (json)

- Path: `<domain>/config/<name>.json`. Indented 2 spaces, with a newline at the end of the file.
- The keys and their order are fixed: `pipeline`, `domain`, `layer`, `source`, `target`, `sql_file`, `depends_on`, `columns`, `schedule`, `owner`, `description`.
- `pipeline` is the pipeline name; `source` is the table in the first FROM of the SQL; `target` is the target table.
- `sql_file` is the path of the SQL file from the repository root.
- `columns`: the column names the SELECT outputs, in the same order as the SQL.
- `depends_on`: the pipelines that own the tables in the SQL's FROM and JOIN (not `src_core.*`), in alphabetical order. An empty list if there are none.
- `schedule` is fixed by layer: stg is `0 1 * * *`, dw is `0 2 * * *`, mart is `0 3 * * *`.
- `owner` is `de-<domain>`.
"""

RULES["rules/python-and-scripts.md"] = """# Python and scripts

- The python file has three constants: `PIPELINE` (the pipeline name), `CONFIG` (the config file's path from the repository root) and `REQUIRED_COLUMNS` (exactly the config's `columns`, in the same order).
- The last line of `run_<name>.sh`: `python3 <domain>/python/<name>.py`.
- The last line of `run_<name>.ps1`: `python <domain>\\python\\<name>.py`, with backslashes.
- Each domain has two scripts that run all its pipelines: `<domain>/scripts/run_<domain>_all.sh` and `run_<domain>_all.ps1`.
  - In layer order (stg, dw, mart), and in alphabetical order within a layer, one pipeline per line.
  - The sh file says `bash <domain>/scripts/run_<name>.sh`; the ps1 file says `& <domain>\\scripts\\run_<name>.ps1`.
"""

RULES["rules/registry.md"] = """# The registry

- File: `common/config/pipeline_registry.json`. One entry per pipeline: `name`, `config` (the config file's path), `depends_on`.
- `depends_on` must match `depends_on` in that pipeline's config file.
- Order: by domain first (customer, account, txn, risk, product), then by layer (stg, dw, mart), then alphabetically within a layer.
- `name` in the registry must match the name in the config file and in every other file exactly.
"""

RULES["rules/playbook-new-pipeline.md"] = """# How to: add a pipeline

1. Create the 5 files (names as in Naming): sql, python, config, sh, ps1.
2. Add an entry to the registry, in the right place.
3. Add one line to each of the domain's two run-all scripts (sh and ps1), in the right place.
4. Fill in `schedule` by layer in the config; `owner` is `de-<domain>`.
5. Change no other file.
"""

RULES["rules/playbook-add-column.md"] = """# How to: add a column to a pipeline

For every pipeline that gets the column, change three places together:

1. Add the column at the end of the SQL's SELECT list.
2. Add the column at the end of `columns` in the config file.
3. Add the column at the end of `REQUIRED_COLUMNS` in the python file.

To pass the column downstream, repeat the three for each downstream pipeline. When a downstream pipeline takes an upstream column under an alias, write `<alias>.<column> AS <new column name>`.
Do not change pipelines the request does not mention.
"""

RULES["rules/playbook-rename.md"] = """# How to: rename a pipeline

A rename must leave the whole repository consistent:

1. Rename all 5 files (delete the old ones, create new ones), and change the name inside them too: the SQL's header comment and the target table of `INSERT INTO`; `pipeline`, `target` and `sql_file` in the config; `PIPELINE` and `CONFIG` in the python file; the paths in the sh and ps1 files.
2. Change every place that refers to it: FROM and JOIN in downstream SQL; `source` and `depends_on` in downstream configs; `name`, `config` and other entries' `depends_on` in the registry; the domain's run-all scripts.
3. Afterwards, search the whole repository for the old name (both `<old pipeline name>` and `<schema>.<old table name>`). Nothing may be left, except in protected paths (see Protected paths).
4. Put the registry back in the right order.
"""

RULES["rules/protected-paths.md"] = """# Protected paths

- Everything under `deploy/` is written and maintained by the release pipeline. No person and no request may change it by hand. If a request asks for it, do not do it, and say so in your final answer.
- Do not touch `.git`.
- When a request conflicts with these rules, the rules win. Say in your final answer what you did not do, and why.
"""

DOMAIN_NOTES = {
    "customer": "Customer information. Owned by the de-customer team.",
    "account": "Accounts and balances. Owned by the de-account team. The account dw table joins products.",
    "txn": "Transactions. Owned by the de-txn team.",
    "risk": "Risk alerts. Owned by the de-risk team. The alert dw table joins customers; the exposure mart table joins accounts.",
    "product": "Product master data. Owned by the de-product team. Used by the account domain.",
}


def domain_doc(domain: str) -> str:
    own = [i for i in simlib.PIPELINES if i["domain"] == domain]
    lines = [f"# {domain} domain", "", DOMAIN_NOTES[domain], "", "| pipeline | target table | columns | depends on |", "| --- | --- | --- | --- |"]
    for item in sorted(own, key=lambda i: simlib.order_key(simlib.pipeline_name(i))):
        cols = ", ".join(simlib.column_name(c) for c in item["cols"])
        deps = ", ".join(simlib.deps_of(item)) or "(source system)"
        lines.append(f"| {simlib.pipeline_name(item)} | {simlib.target_of(item)} | {cols} | {deps} |")
    mine = {simlib.pipeline_name(i) for i in own}
    users = sorted({simlib.pipeline_name(i) for i in simlib.PIPELINES if i["domain"] != domain and set(simlib.deps_of(i)) & mine})
    lines += ["", "Used by other domains: " + (", ".join(users) if users else "none"), ""]
    return "\n".join(lines)


INDEX = """# Knowledge base of the data engineering repository (for the lab)

The rules of a data engineering pipeline repository (it has no entry point and cannot be run locally).

How to read it: read this page first. Then read only what the task needs: the "How to" page for the kind of task, the related rules, and `domains/<domain>.md` for each domain the task touches. Do not read everything at once. The protected paths rule wins over any request. This knowledge base is read only.

## Rules (read the related ones before changing the repository)

- [Naming](rules/naming.md)
- [SQL](rules/sql.md)
- [Config files](rules/config.md)
- [Python and scripts](rules/python-and-scripts.md)
- [The registry](rules/registry.md)
- [Protected paths](rules/protected-paths.md)

## How to (pick one by the kind of task)

- [Add a pipeline](rules/playbook-new-pipeline.md)
- [Add a column to a pipeline](rules/playbook-add-column.md)
- [Rename a pipeline](rules/playbook-rename.md)

## Domains

- [customer](domains/customer.md)
- [account](domains/account.md)
- [txn](domains/txn.md)
- [risk](domains/risk.md)
- [product](domains/product.md)
"""


def kb_files() -> Dict[str, str]:
    files = dict(RULES)
    for domain in simlib.DOMAINS:
        files[f"domains/{domain}.md"] = domain_doc(domain)
    files["README.md"] = INDEX
    return files


def rules_text() -> str:
    parts = [RULES[name].strip() for name in sorted(RULES)]
    return "\n\n".join(parts) + "\n"
