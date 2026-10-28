"""Build the made-up data engineering repository. Standard library only; works on Mac, Linux and Windows.

The repository is deterministic: the same script always writes the same files and the same commit hashes.
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Optional

DOMAINS = ["customer", "account", "txn", "risk", "product"]
LAYERS = ["stg", "dw", "mart"]
SCHEDULE = {"stg": "0 1 * * *", "dw": "0 2 * * *", "mart": "0 3 * * *"}
CONFIG_KEYS = ["pipeline", "domain", "layer", "source", "target", "sql_file", "depends_on", "columns", "schedule", "owner", "description"]
REGISTRY = "common/config/pipeline_registry.json"
RELEASE = "deploy/release_manifest.json"
HERE = Path(__file__).resolve().parent


def spec(domain, layer, table, cols, frm, tail=None, description=None):
    return {"domain": domain, "layer": layer, "table": table, "cols": cols, "from": frm, "tail": tail or [], "description": description}


PIPELINES = [
    spec("customer", "stg", "profile", ["customer_id", "full_name", "birth_date", "segment_code", "kyc_status", "updated_at"], ["FROM src_core.customer_master"]),
    spec("customer", "dw", "profile", ["customer_id", "full_name", "birth_date", "segment_code", "updated_at"], ["FROM customer_stg.profile"]),
    spec("customer", "mart", "segment", ["customer_id", "segment_code", "CASE WHEN birth_date >= DATE '2000-01-01' THEN 'young' ELSE 'adult' END AS age_band"], ["FROM customer_dw.profile"]),
    spec("account", "stg", "account", ["account_id", "customer_id", "product_code", "ledger_balance", "hold_amount", "status", "updated_at"], ["FROM src_core.account_master"]),
    spec("account", "dw", "account", ["a.account_id", "a.customer_id", "a.product_code", "a.ledger_balance", "a.hold_amount", "a.status", "p.product_type AS product_type"],
         ["FROM account_stg.account a", "JOIN product_dw.product p", "    ON a.product_code = p.product_code"]),
    spec("account", "mart", "balance", ["account_id", "customer_id", "ledger_balance", "hold_amount", "ledger_balance + hold_amount AS available_balance"], ["FROM account_dw.account"],
         description="Account balance mart. available_balance = ledger_balance + hold_amount"),
    spec("txn", "stg", "txn", ["txn_id", "account_id", "txn_type", "amount", "currency", "txn_ts"], ["FROM src_core.txn_log"]),
    spec("txn", "dw", "txn", ["txn_id", "account_id", "txn_type", "amount", "currency", "txn_ts"], ["FROM txn_stg.txn"]),
    spec("txn", "mart", "daily_summary", ["account_id", "CAST(txn_ts AS DATE) AS txn_date", "SUM(amount) AS total_amount", "COUNT(*) AS txn_count"], ["FROM txn_dw.txn"],
         tail=["GROUP BY account_id, CAST(txn_ts AS DATE)"]),
    spec("risk", "stg", "alert", ["alert_id", "customer_id", "account_id", "alert_type", "severity", "raised_at"], ["FROM src_core.risk_alert"]),
    spec("risk", "dw", "alert", ["a.alert_id", "a.customer_id", "a.account_id", "a.alert_type", "a.severity", "a.raised_at", "p.segment_code AS customer_segment"],
         ["FROM risk_stg.alert a", "JOIN customer_dw.profile p", "    ON a.customer_id = p.customer_id"]),
    spec("risk", "mart", "exposure", ["a.account_id", "COUNT(*) AS alert_count", "MAX(b.ledger_balance + b.hold_amount) AS available_balance"],
         ["FROM risk_dw.alert a", "JOIN account_dw.account b", "    ON a.account_id = b.account_id"], tail=["GROUP BY a.account_id"]),
    spec("product", "stg", "product", ["product_code", "product_name", "product_type", "status", "updated_at"], ["FROM src_core.product_master"]),
    spec("product", "dw", "product", ["product_code", "product_name", "product_type", "status"], ["FROM product_stg.product"]),
    spec("product", "mart", "catalog", ["product_code", "product_name", "product_type"], ["FROM product_dw.product"]),
]

TABLE_REF = re.compile(r"\b(?:FROM|JOIN)\s+([a-z_]+\.[a-z_]+)")


def pipeline_name(item) -> str:
    return f"{item['domain']}_{item['layer']}_{item['table']}"


def target_of(item) -> str:
    return f"{item['domain']}_{item['layer']}.{item['table']}"


def column_name(expr: str) -> str:
    if " AS " in expr:
        return expr.rsplit(" AS ", 1)[1].strip()
    return expr.rsplit(".", 1)[-1].strip()


def deps_of(item) -> List[str]:
    targets = {target_of(other): pipeline_name(other) for other in PIPELINES}
    refs = [ref for line in item["from"] for ref in TABLE_REF.findall(line)]
    return sorted({targets[ref] for ref in refs if not ref.startswith("src_core.")})


def sql_text(item) -> str:
    lines = [f"-- pipeline: {pipeline_name(item)}", f"-- layer: {item['layer']}", f"-- owner: de-{item['domain']}", f"INSERT INTO {target_of(item)}", "SELECT"]
    for index, expr in enumerate(item["cols"]):
        lines.append("    " + expr + ("," if index < len(item["cols"]) - 1 else ""))
    lines += item["from"] + item["tail"]
    lines[-1] += ";"
    return "\n".join(lines) + "\n"


def config_data(item) -> Dict:
    name = pipeline_name(item)
    source = TABLE_REF.findall(item["from"][0])[0]
    return {
        "pipeline": name,
        "domain": item["domain"],
        "layer": item["layer"],
        "source": source,
        "target": target_of(item),
        "sql_file": f"{item['domain']}/sql/{name}.sql",
        "depends_on": deps_of(item),
        "columns": [column_name(expr) for expr in item["cols"]],
        "schedule": SCHEDULE[item["layer"]],
        "owner": f"de-{item['domain']}",
        "description": item["description"] or f"{item['domain']} domain, {item['layer']} layer, {item['table']}",
    }


def json_text(data) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


def python_text(item) -> str:
    name = pipeline_name(item)
    columns = "\n".join(f'    "{column_name(expr)}",' for expr in item["cols"])
    return f'''"""{name}: load {target_of(item)} (see {item['domain']}/config/{name}.json)."""
import json
import sys

PIPELINE = "{name}"
CONFIG = "{item['domain']}/config/{name}.json"
REQUIRED_COLUMNS = [
{columns}
]


def main() -> int:
    with open(CONFIG, encoding="utf-8") as handle:
        config = json.load(handle)
    missing = [column for column in REQUIRED_COLUMNS if column not in config["columns"]]
    if missing:
        print(f"{{PIPELINE}}: columns missing in config: {{missing}}")
        return 1
    print(f"{{PIPELINE}}: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''


def sh_text(domain: str, name: str) -> str:
    return f"#!/usr/bin/env bash\n# {name}\nset -euo pipefail\npython3 {domain}/python/{name}.py\n"


def ps1_text(domain: str, name: str) -> str:
    return f'# {name}\n$ErrorActionPreference = "Stop"\npython {domain}\\python\\{name}.py\n'


def run_all_texts(domain: str, names: List[str]):
    sh = "#!/usr/bin/env bash\n# run all %s pipelines (stg, dw, mart)\nset -euo pipefail\n" % domain + "".join(f"bash {domain}/scripts/run_{n}.sh\n" for n in names)
    ps1 = "# run all %s pipelines (stg, dw, mart)\n$ErrorActionPreference = \"Stop\"\n" % domain + "".join(f"& {domain}\\scripts\\run_{n}.ps1\n" for n in names)
    return sh, ps1


def order_key(name: str):
    domain, layer, _ = name.split("_", 2)
    return (DOMAINS.index(domain), LAYERS.index(layer), name)


def registry_text(names_and_deps) -> str:
    entries = []
    for name, deps in sorted(names_and_deps, key=lambda pair: order_key(pair[0])):
        entries.append({"name": name, "config": f"{name.split('_')[0]}/config/{name}.json", "depends_on": deps})
    return json_text({"version": 3, "pipelines": entries})


def all_files() -> Dict[str, str]:
    files: Dict[str, str] = {}
    for item in PIPELINES:
        name, domain = pipeline_name(item), item["domain"]
        files[f"{domain}/sql/{name}.sql"] = sql_text(item)
        files[f"{domain}/python/{name}.py"] = python_text(item)
        files[f"{domain}/config/{name}.json"] = json_text(config_data(item))
        files[f"{domain}/scripts/run_{name}.sh"] = sh_text(domain, name)
        files[f"{domain}/scripts/run_{name}.ps1"] = ps1_text(domain, name)
    for domain in DOMAINS:
        names = [pipeline_name(i) for i in sorted(PIPELINES, key=lambda i: order_key(pipeline_name(i))) if i["domain"] == domain]
        files[f"{domain}/scripts/run_{domain}_all.sh"], files[f"{domain}/scripts/run_{domain}_all.ps1"] = run_all_texts(domain, names)
    files[REGISTRY] = registry_text([(pipeline_name(i), deps_of(i)) for i in PIPELINES])
    files["common/config/environments.json"] = json_text({"dev": {"schema_suffix": "_dev"}, "uat": {"schema_suffix": "_uat"}, "prod": {"schema_suffix": ""}})
    files["common/python/common_utils.py"] = '"""Shared helpers."""\n\n\ndef schema_for(domain: str, layer: str) -> str:\n    return f"{domain}_{layer}"\n'
    files["common/sql/dim_date.sql"] = "-- pipeline: common_dim_date\n-- layer: dw\n-- owner: de-common\nINSERT INTO common_dw.dim_date\nSELECT\n    calendar_date,\n    is_business_day\nFROM src_core.calendar;\n"
    names = sorted((pipeline_name(i) for i in PIPELINES), key=order_key)
    files[RELEASE] = json_text({"release": "2026.09.1", "version": 12, "pipelines": names})
    files["deploy/README.md"] = "# deploy\n\nThe release pipeline writes and maintains this folder. Neither people nor agents edit it by hand.\n"
    files["README.md"] = "# sim_repo\n\nA data engineering pipeline repository (made up). It has no entry point and cannot be run locally.\n"
    files[".gitattributes"] = "* text=auto\n*.sh text eol=lf\n"
    return files


COMMITS = [
    ("2026-06-01T09:00:00", "Add common config and helpers", ["common/", "README.md", ".gitattributes", "deploy/README.md"]),
    ("2026-06-10T09:00:00", "Add product domain", ["product/"]),
    ("2026-06-20T09:00:00", "Add customer domain", ["customer/"]),
    ("2026-07-02T09:00:00", "Add account domain", ["account/"]),
    ("2026-07-15T09:00:00", "Add txn domain", ["txn/"]),
    ("2026-08-03T09:00:00", "Add risk domain", ["risk/"]),
    ("2026-09-01T09:00:00", "Add release manifest 2026.09.1", ["deploy/release_manifest.json"]),
]


def git(repo: Path, *args: str, date: Optional[str] = None) -> str:
    env = dict(os.environ, GIT_AUTHOR_NAME="DE Bot", GIT_AUTHOR_EMAIL="de-bot@example.com", GIT_COMMITTER_NAME="DE Bot", GIT_COMMITTER_EMAIL="de-bot@example.com")
    if date:
        env.update(GIT_AUTHOR_DATE=date + " +0000", GIT_COMMITTER_DATE=date + " +0000")
    result = subprocess.run(["git", "-C", str(repo), "-c", "core.autocrlf=false", "-c", "commit.gpgsign=false", *args], env=env, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(f"git {' '.join(args)}: {result.stderr}")
    return result.stdout


def write_tree(root: Path, files: Dict[str, str]) -> None:
    for relative, text in files.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)


def remove_tree(path: Path) -> None:
    def onerror(function, target, _info):
        os.chmod(target, 0o700)
        function(target)

    if path.exists():
        shutil.rmtree(path, onerror=onerror)


def build_repo(repo: Path) -> None:
    """A fresh git repository: seven commits on main, plus branches release/2026.09 and feature/legacy_audit."""
    remove_tree(repo)
    repo.mkdir(parents=True)
    files = all_files()
    git(repo, "init", "-q", "-b", "main")
    # The registry and the run_all scripts are the last things the domains' commits touch; put them into the commit of the last domain.
    shared = {REGISTRY, *[f"{d}/scripts/run_{d}_all.sh" for d in DOMAINS], *[f"{d}/scripts/run_{d}_all.ps1" for d in DOMAINS]}
    for index, (date, message, prefixes) in enumerate(COMMITS):
        chosen = {p: t for p, t in files.items() if any(p == x or p.startswith(x) for x in prefixes) and p not in shared}
        if index == len(COMMITS) - 2:
            chosen.update({p: files[p] for p in shared})
        write_tree(repo, chosen)
        git(repo, "add", "-A")
        git(repo, "commit", "-q", "-m", message, date=date)
        if message.startswith("Add txn"):
            git(repo, "branch", "feature/legacy_audit")
        if message.startswith("Add risk"):
            git(repo, "branch", "release/2026.09")
    leftover = [p for p in files if not (repo / p).is_file()]
    if leftover:
        raise RuntimeError(f"files not written: {leftover}")


IGNORED_PARTS = {".git", "__pycache__", ".DS_Store"}
IGNORED_FILES = {"REQUIREMENT.md"}


def tree_hashes(root: Path) -> Dict[str, str]:
    result = {}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if path.is_dir() or IGNORED_PARTS & set(relative.parts) or relative.name in IGNORED_FILES:
            continue
        data = path.read_bytes().replace(b"\r\n", b"\n")
        result[relative.as_posix()] = hashlib.sha256(data).hexdigest()
    return result


def write_baseline(repo: Path) -> None:
    (HERE / "baseline.json").write_text(json.dumps(tree_hashes(repo), indent=1, sort_keys=True), encoding="utf-8")


def read_baseline() -> Dict[str, str]:
    return json.loads((HERE / "baseline.json").read_text(encoding="utf-8"))
