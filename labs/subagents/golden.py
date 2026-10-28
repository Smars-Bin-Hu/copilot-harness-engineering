"""The right answer to each task, and broken versions of it. Used only to prove the scoring script can be trusted.

The answers are written as literal text and string replacements, not with simlib's generators, so the checks and the answers cannot bend to each other.
"""
import json
import os
from pathlib import Path
from typing import Callable, Dict, List


def read(root: Path, path: str) -> str:
    return (root / path).read_text(encoding="utf-8")


def write(root: Path, path: str, text: str) -> None:
    target = root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    with open(target, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def sub(root: Path, path: str, old: str, new: str, count: int = 1) -> None:
    text = read(root, path)
    assert old in text, (path, old)
    write(root, path, text.replace(old, new, count))


def remove(root: Path, path: str) -> None:
    (root / path).unlink()


T1_FILES = {
    "account/sql/account_stg_credit_line.sql": """-- pipeline: account_stg_credit_line
-- layer: stg
-- owner: de-account
INSERT INTO account_stg.credit_line
SELECT
    account_id,
    line_type,
    line_amount,
    currency,
    updated_at
FROM src_core.credit_line;
""",
    "account/python/account_stg_credit_line.py": '''"""account_stg_credit_line: load account_stg.credit_line (see account/config/account_stg_credit_line.json)."""
import json
import sys

PIPELINE = "account_stg_credit_line"
CONFIG = "account/config/account_stg_credit_line.json"
REQUIRED_COLUMNS = [
    "account_id",
    "line_type",
    "line_amount",
    "currency",
    "updated_at",
]


def main() -> int:
    with open(CONFIG, encoding="utf-8") as handle:
        config = json.load(handle)
    missing = [column for column in REQUIRED_COLUMNS if column not in config["columns"]]
    if missing:
        print(f"{PIPELINE}: columns missing in config: {missing}")
        return 1
    print(f"{PIPELINE}: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
''',
    "account/config/account_stg_credit_line.json": """{
  "pipeline": "account_stg_credit_line",
  "domain": "account",
  "layer": "stg",
  "source": "src_core.credit_line",
  "target": "account_stg.credit_line",
  "sql_file": "account/sql/account_stg_credit_line.sql",
  "depends_on": [],
  "columns": [
    "account_id",
    "line_type",
    "line_amount",
    "currency",
    "updated_at"
  ],
  "schedule": "0 1 * * *",
  "owner": "de-account",
  "description": "account domain, stg layer, credit_line"
}
""",
    "account/scripts/run_account_stg_credit_line.sh": "#!/usr/bin/env bash\n# account_stg_credit_line\nset -euo pipefail\npython3 account/python/account_stg_credit_line.py\n",
    "account/scripts/run_account_stg_credit_line.ps1": '# account_stg_credit_line\n$ErrorActionPreference = "Stop"\npython account\\python\\account_stg_credit_line.py\n',
}


def t1(root: Path) -> None:
    for path, text in T1_FILES.items():
        write(root, path, text)
    sub(root, "common/config/pipeline_registry.json", '''    {
      "name": "account_dw_account",''', '''    {
      "name": "account_stg_credit_line",
      "config": "account/config/account_stg_credit_line.json",
      "depends_on": []
    },
    {
      "name": "account_dw_account",''')
    sub(root, "account/scripts/run_account_all.sh", "bash account/scripts/run_account_stg_account.sh\n", "bash account/scripts/run_account_stg_account.sh\nbash account/scripts/run_account_stg_credit_line.sh\n")
    sub(root, "account/scripts/run_account_all.ps1", "& account\\scripts\\run_account_stg_account.ps1\n", "& account\\scripts\\run_account_stg_account.ps1\n& account\\scripts\\run_account_stg_credit_line.ps1\n")


def add_column(root: Path, domain: str, name: str, column: str, expr: str) -> None:
    sql = f"{domain}/sql/{name}.sql"
    text = read(root, sql)
    head, rest = text.split("\nFROM ", 1)
    lines = head.split("\n")
    lines[-1] += ","
    lines.append("    " + expr)
    write(root, sql, "\n".join(lines) + "\nFROM " + rest)
    config = f"{domain}/config/{name}.json"
    data = json.loads(read(root, config))
    data["columns"].append(column)
    write(root, config, json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    py = f"{domain}/python/{name}.py"
    text = read(root, py)
    marker = "]\n\n\ndef main"
    assert marker in text
    write(root, py, text.replace(marker, f'    "{column}",\n]\n\n\ndef main', 1))


def t2(root: Path) -> None:
    add_column(root, "customer", "customer_dw_profile", "kyc_status", "kyc_status")
    add_column(root, "customer", "customer_mart_segment", "kyc_status", "kyc_status")
    add_column(root, "risk", "risk_dw_alert", "customer_kyc_status", "p.kyc_status AS customer_kyc_status")


def t3(root: Path) -> None:
    old, new = "product_dw_product", "product_dw_item"
    for path in ["product/sql/%s.sql", "product/python/%s.py", "product/config/%s.json", "product/scripts/run_%s.sh", "product/scripts/run_%s.ps1"]:
        text = read(root, path % old)
        remove(root, path % old)
        write(root, path % new, text.replace(old, new).replace("product_dw.product", "product_dw.item"))
    for path in ("product/sql/product_mart_catalog.sql", "product/config/product_mart_catalog.json", "account/sql/account_dw_account.sql", "account/config/account_dw_account.json", "common/config/pipeline_registry.json", "product/scripts/run_product_all.sh", "product/scripts/run_product_all.ps1"):
        write(root, path, read(root, path).replace(old, new).replace("product_dw.product", "product_dw.item"))
    # the registry order inside the product domain: stg, dw, mart (item stays in the dw slot), nothing to move; the same for the run_all scripts


def t4(root: Path) -> None:
    sub(root, "account/sql/account_mart_balance.sql", "ledger_balance + hold_amount AS", "ledger_balance - hold_amount AS")
    sub(root, "risk/sql/risk_mart_exposure.sql", "MAX(b.ledger_balance + b.hold_amount)", "MAX(b.ledger_balance - b.hold_amount)")
    sub(root, "account/config/account_mart_balance.json", "ledger_balance + hold_amount", "ledger_balance - hold_amount")


GOLDEN: Dict[str, Callable[[Path], None]] = {"T1": t1, "T2": t2, "T3": t3, "T4": t4}


def m(task: str, name: str, fails: List[str], function: Callable[[Path], None]):
    return (task, name, fails, function)


def after(task: str, extra: Callable[[Path], None]) -> Callable[[Path], None]:
    def run(root: Path) -> None:
        GOLDEN[task](root)
        extra(root)

    return run


def t1_wrong_schedule(root: Path) -> None:
    sub(root, "account/config/account_stg_credit_line.json", "0 1 * * *", "0 2 * * *")


def t1_no_ps1(root: Path) -> None:
    remove(root, "account/scripts/run_account_stg_credit_line.ps1")


def t1_not_registered(root: Path) -> None:
    sub(root, "common/config/pipeline_registry.json", '''    {
      "name": "account_stg_credit_line",
      "config": "account/config/account_stg_credit_line.json",
      "depends_on": []
    },
''', "")


def t1_run_all_ps1_missing(root: Path) -> None:
    sub(root, "account/scripts/run_account_all.ps1", "& account\\scripts\\run_account_stg_credit_line.ps1\n", "")


def t1_registry_order(root: Path) -> None:
    text = read(root, "common/config/pipeline_registry.json")
    block = '''    {
      "name": "account_stg_credit_line",
      "config": "account/config/account_stg_credit_line.json",
      "depends_on": []
    },
'''
    write(root, "common/config/pipeline_registry.json", text.replace(block, "").replace('''    {
      "name": "txn_stg_txn",''', block + '''    {
      "name": "txn_stg_txn",'''))


def t1_py_columns(root: Path) -> None:
    sub(root, "account/python/account_stg_credit_line.py", '    "currency",\n', "")


def t1_extra_file(root: Path) -> None:
    sub(root, "customer/config/customer_stg_profile.json", '"description": "customer domain, stg layer, profile"', '"description": "customer domain, stg layer, profile v2"')


def t2_no_python(root: Path) -> None:
    sub(root, "risk/python/risk_dw_alert.py", '    "customer_kyc_status",\n', "")


def t2_no_mart(root: Path) -> None:
    sub(root, "customer/sql/customer_mart_segment.sql", ",\n    kyc_status\nFROM", "\nFROM")
    sub(root, "customer/config/customer_mart_segment.json", ',\n    "kyc_status"\n', "\n")
    sub(root, "customer/python/customer_mart_segment.py", '    "kyc_status",\n', "")


def t2_wrong_name(root: Path) -> None:
    sub(root, "risk/sql/risk_dw_alert.sql", "AS customer_kyc_status", "AS kyc_status")


def t2_touch_stg(root: Path) -> None:
    sub(root, "customer/config/customer_stg_profile.json", '"description": "customer domain, stg layer, profile"', '"description": "x"')


def t2_not_last(root: Path) -> None:
    sub(root, "customer/sql/customer_dw_profile.sql", "    full_name,\n", "    kyc_status,\n    full_name,\n")
    sub(root, "customer/sql/customer_dw_profile.sql", "    updated_at,\n    kyc_status\n", "    updated_at\n")


def t3_leftover_sql(root: Path) -> None:
    sub(root, "account/sql/account_dw_account.sql", "product_dw.item", "product_dw.product")


def t3_no_registry(root: Path) -> None:
    sub(root, "common/config/pipeline_registry.json", "product_dw_item", "product_dw_product", 2)


def t3_touch_deploy(root: Path) -> None:
    sub(root, "deploy/release_manifest.json", "product_dw_product", "product_dw_item")


def t3_ps1_path(root: Path) -> None:
    sub(root, "product/scripts/run_product_dw_item.ps1", "product_dw_item.py", "product_dw_product.py")


def t3_keep_old(root: Path) -> None:
    write(root, "product/sql/product_dw_product.sql", "-- old\n")


def t3_no_run_all(root: Path) -> None:
    sub(root, "product/scripts/run_product_all.sh", "run_product_dw_item.sh", "run_product_dw_product.sh")


def t4_one_only(root: Path) -> None:
    sub(root, "risk/sql/risk_mart_exposure.sql", "MAX(b.ledger_balance - b.hold_amount)", "MAX(b.ledger_balance + b.hold_amount)")


def t4_deploy(root: Path) -> None:
    sub(root, "deploy/release_manifest.json", '"version": 12', '"version": 13')


def t4_description(root: Path) -> None:
    sub(root, "account/config/account_mart_balance.json", "ledger_balance - hold_amount", "ledger_balance + hold_amount")


MUTANTS = [
    m("T1", "wrong schedule", ["G5", "T1.2"], after("T1", t1_wrong_schedule)),
    m("T1", "no ps1", ["G2", "T1.1"], after("T1", t1_no_ps1)),
    m("T1", "not registered", ["G7", "T1.4"], after("T1", t1_not_registered)),
    m("T1", "run-all ps1 line missing", ["G8", "T1.5"], after("T1", t1_run_all_ps1_missing)),
    m("T1", "registry out of order", ["G7"], after("T1", t1_registry_order)),
    m("T1", "python misses a column", ["G4"], after("T1", t1_py_columns)),
    m("T1", "changed another file", ["S"], after("T1", t1_extra_file)),
    m("T2", "risk python not changed", ["G4", "T2.3"], after("T2", t2_no_python)),
    m("T2", "mart not changed", ["T2.2"], after("T2", t2_no_mart)),
    m("T2", "wrong column name", ["T2.3"], after("T2", t2_wrong_name)),
    m("T2", "changed stg too", ["S"], after("T2", t2_touch_stg)),
    m("T2", "new column not at the end", ["T2.1"], after("T2", t2_not_last)),
    m("T3", "old name left in downstream SQL", ["G6", "T3.4", "T3.5"], after("T3", t3_leftover_sql)),
    m("T3", "registry not fully renamed", ["G7", "T3.4", "T3.6"], after("T3", t3_no_registry)),
    m("T3", "changed deploy", ["G9", "S"], after("T3", t3_touch_deploy)),
    m("T3", "ps1 path not changed", ["G8", "T3.4"], after("T3", t3_ps1_path)),
    m("T3", "old files kept", ["T3.1", "G2"], after("T3", t3_keep_old)),
    m("T3", "run-all scripts not changed", ["G8", "T3.4"], after("T3", t3_no_run_all)),
    m("T4", "fixed only one place", ["T4.1", "T4.2"], after("T4", t4_one_only)),
    m("T4", "changed deploy", ["G9", "T4.4", "S"], after("T4", t4_deploy)),
    m("T4", "config description not fixed", ["T4.3", "T4.2"], after("T4", t4_description)),
]
