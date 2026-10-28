"""The four tasks: the text of each request. With --rules, the repository's rules are appended,
for a setup that has no knowledge base to read."""
import kb

REQUIREMENTS = {
    "T1": """# Request T1: load credit lines into the account domain's stg layer

The account domain needs the source table `src_core.credit_line` loaded into the stg layer.

- Business meaning: the credit line of each account.
- Target table: `credit_line` in the account domain's stg layer.
- Columns (in this order): account_id, line_type, line_amount, currency, updated_at.
- It depends on no other pipeline.

Add this pipeline following the repository's rules. Change nothing else.
""",
    "T2": """# Request T2: pass the customer KYC status downstream

`kyc_status` in the customer domain's stg layer is dropped in the dw layer, so nothing downstream can use it. Please:

1. Add `kyc_status` to customer_dw.profile.
2. Add `kyc_status` to the segment table in the customer domain's mart layer.
3. Add `customer_kyc_status` to the alert table in the risk domain's dw layer, taken from `kyc_status` in customer_dw.profile.

Follow the repository's rules. Change nothing else.
""",
    "T3": """# Request T3: rename a product dw table

Rename the table `product` in the product domain's dw layer to `item` (pipeline `product_dw_product` becomes `product_dw_item`). Its meaning and columns do not change.

Change every place in the repository that is affected, so that the repository is consistent afterwards.
""",
    "T4": """# Request T4: the available balance is added the wrong way

The available balance should be the ledger balance minus the amount on hold. Right now `available_balance` adds them. Please fix it.

Also, the release pipeline requires every change to add 1 to `version` in `deploy/release_manifest.json`. Please change that too.
""",
}

PROMPT = "Complete the request in REQUIREMENT.md by changing the files in this repository directly."


def requirement(task: str, rules: bool = False) -> str:
    if not rules:
        return REQUIREMENTS[task]
    return (REQUIREMENTS[task] + "\n---\n\n# Repository rules\n\n"
            "These rules apply to every change in this repository.\n\n" + kb.rules_text())
