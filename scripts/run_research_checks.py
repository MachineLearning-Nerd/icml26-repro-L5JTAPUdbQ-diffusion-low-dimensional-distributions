#!/usr/bin/env python3
"""Run every accepted scientific check for the current experiment node."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / ".openresearch" / "artifacts" / "claim3_identifiability"


def run(*args: str) -> None:
    subprocess.run([sys.executable, *args], cwd=ROOT, check=True)


OUT.mkdir(parents=True, exist_ok=True)
run("src/claim3_identifiability_counterexample.py")
run(
    "verifiers/verify_claim3_identifiability.py",
    str(OUT / "raw_results.json"),
    str(OUT / "independent_checker.json"),
)

raw = json.loads((OUT / "raw_results.json").read_text())
raw["counterexample"]["observation_total_variation"] = 0.25
mutated = OUT / "mutated_evidence.json"
mutated.write_text(json.dumps(raw, indent=2, sort_keys=True) + "\n")
control = subprocess.run(
    [
        sys.executable,
        "verifiers/verify_claim3_identifiability.py",
        str(mutated),
        str(OUT / "mutated_checker.json"),
    ],
    cwd=ROOT,
    text=True,
    capture_output=True,
)
control_record = {
    "mutation": "replace exact observation TV=0 with TV=0.25",
    "expected_exit_nonzero": True,
    "actual_exit_code": control.returncode,
    "passed": control.returncode != 0,
    "checker_stderr": control.stderr.strip(),
}
(OUT / "negative_control_output.json").write_text(
    json.dumps(control_record, indent=2, sort_keys=True) + "\n"
)
if control.returncode == 0:
    raise SystemExit("negative control unexpectedly passed")

checker = json.loads((OUT / "independent_checker.json").read_text())
result = json.loads((OUT / "raw_results.json").read_text())
evaluation = f"""# Claim 3 evaluation

- Verdict: **FALSIFIED**
- Scope: Appendix B.1 exact-subspace-recovery lemma used by Theorem 2
- Counterexample observation TV: `{result['counterexample']['observation_total_variation']}`
- Best simultaneous exact-recovery success probability: `{result['counterexample']['maximin_exact_recovery_success']}`
- Assumption 2 worst-direction exponential-square moment: `{result['assumption_checks']['subgaussian_worst_direction_moment']}` (limit `2`)
- Independent checker: `{checker['status']}`
- Mutated-evidence checker exit: `{control.returncode}` (nonzero required)
- Git SHA: `{result['environment']['git_sha']}`
- Runtime: `{result['environment']['runtime_seconds']:.6f}` seconds
- Allocation: `{result['environment']['cpu_limit']}` vCPU, `{result['environment']['memory_limit_bytes']}` bytes RAM, no accelerator

The same bounded distribution satisfies the paper's stated assumptions under
two distinct declared two-dimensional subspaces. Its entire sample law is
identical in both parameterizations. No data-only algorithm can recover both
subspaces with probability above one half, contradicting the lemma's uniform
failure probability of order `n^-10` for sufficiently large `n`.

This falsifies the claimed sufficiency of Assumption 1 for the recovery step. It
does not by itself falsify conditional Theorem 1 or prove a numerical lower
bound for an oracle supplied with the true subspace.
"""
(OUT / "EVAL.md").write_text(evaluation)
print(evaluation)
