#!/usr/bin/env python3
"""Persist exact evaluator-review markers from completed OpenResearch runs."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_JSON = ROOT / "release/EVALUATOR_RED_TEAM.json"
OUTPUT_MD = ROOT / "release/EVALUATOR_RED_TEAM.md"
ROUNDS = [
    {
        "label": "round_1_before_fixes",
        "run_id": "0bf1fc1d-4741-4654-a8ee-9b68e66d69c2",
        "hf_job": "DineshAI/6a6e3877a00abefd4b28bd46",
        "git_sha": "d825d66e84b0a416ed735d27e920e490b5dc4187",
    },
    {
        "label": "round_2_after_fixes",
        "run_id": "9ec85de3-636f-4ecb-ab7b-d2ffc70b6316",
        "hf_job": "DineshAI/6a6e3ad0a00abefd4b28bd76",
        "git_sha": "214ef5e8fea680f32be066e40f31bd3bfd6ebaea",
    },
]


def reviewer_result(run_id: str) -> dict:
    completed = subprocess.run(
        ["orx", "logs", run_id, "--bytes", "400000"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    prefix = "EVALUATOR_REVIEW_JSON="
    markers = [line[len(prefix) :] for line in completed.stdout.splitlines() if line.startswith(prefix)]
    if len(markers) != 1:
        raise ValueError(f"expected one evaluator marker for {run_id}, found {len(markers)}")
    return json.loads(markers[0])


def main() -> None:
    rounds = []
    for metadata in ROUNDS:
        rounds.append({**metadata, "review": reviewer_result(metadata["run_id"])})

    payload = {
        "schema_version": 1,
        "review_rule": "Start at README/logbook.json and use only reachable candidate files; repository knowledge is forbidden.",
        "rounds": rounds,
    }
    OUTPUT_JSON.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    first, second = rounds
    issue_lines = "\n".join(
        f"- `{issue['code']}` — {issue['detail']}" for issue in first["review"]["issues"]
    )
    markdown = f"""# Evaluator-blind pre-publication review

The reviewer began only at `README.md` and `logbook.json`, downloaded the
protected revision afresh, traversed the candidate page tree and direct links,
and did not use unpublished repository knowledge. The exact files opened and
all release-gate reads are recorded in
[`EVALUATOR_RED_TEAM.json`](EVALUATOR_RED_TEAM.json).

## Round 1 — FAIL before fixes

- Run: `{first['run_id']}`
- HF job: `{first['hf_job']}` (`cpu-upgrade`, no accelerator)
- Git SHA: `{first['git_sha']}`
- Reviewer status: **{first['review']['status']}**
- Files opened through evaluator traversal: `{len(first['review']['reviewer_opened_files'])}`
- Findings: `{len(first['review']['issues'])}`

{issue_lines}

## Round 2 — PASS after fixes

- Run: `{second['run_id']}`
- HF job: `{second['hf_job']}` (`cpu-upgrade`, no accelerator)
- Git SHA: `{second['git_sha']}`
- Reviewer status: **{second['review']['status']}**
- Files opened through evaluator traversal: `{len(second['review']['reviewer_opened_files'])}`
- Findings: `{len(second['review']['issues'])}`
- Protected file subset: `{str(second['review']['protected_file_subset']).lower()}`
- Protected page-tree subset: `{str(second['review']['protected_page_subset']).lower()}`
- Visibility rows complete: `{str(second['review']['visibility_rows_complete']).lower()}`

The packaged release adds this record after Round 2, so a final third HF run
must pass before publication.
"""
    OUTPUT_MD.write_text(markdown)


if __name__ == "__main__":
    main()
