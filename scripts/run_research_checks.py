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

claim5_out = ROOT / ".openresearch" / "artifacts" / "claim5_prior_rate"
claim5_out.mkdir(parents=True, exist_ok=True)
run("src/claim5_primary_proof_chain.py")
run(
    "verifiers/verify_claim5_primary_proof_chain.py",
    str(claim5_out / "raw_results.json"),
    str(claim5_out / "independent_checker.json"),
)
claim5_raw = json.loads((claim5_out / "raw_results.json").read_text())
claim5_raw["rate_cases"][0]["sample_exponent"] = "999"
claim5_mutated = claim5_out / "mutated_evidence.json"
claim5_mutated.write_text(json.dumps(claim5_raw, indent=2, sort_keys=True) + "\n")
claim5_control = subprocess.run(
    [
        sys.executable,
        "verifiers/verify_claim5_primary_proof_chain.py",
        str(claim5_mutated),
        str(claim5_out / "mutated_checker.json"),
    ],
    cwd=ROOT,
    text=True,
    capture_output=True,
)
claim5_control_record = {
    "mutation": "replace the first independently derived sample exponent with 999",
    "expected_exit_nonzero": True,
    "actual_exit_code": claim5_control.returncode,
    "passed": claim5_control.returncode != 0,
    "checker_stderr": claim5_control.stderr.strip(),
}
(claim5_out / "negative_control_output.json").write_text(
    json.dumps(claim5_control_record, indent=2, sort_keys=True) + "\n"
)
if claim5_control.returncode == 0:
    raise SystemExit("Claim 5 negative control unexpectedly passed")

claim5_checker = json.loads((claim5_out / "independent_checker.json").read_text())
claim5_result = json.loads((claim5_out / "raw_results.json").read_text())
claim5_evaluation = f"""# Claim 5 evaluation

- Verdict: **VERIFIED**
- Confidence: **MEDIUM**
- Direct primary source: Cai and Li, arXiv:2503.09583, Theorem 1
- Prior TV exponent: `beta/(d+2 beta)`
- Inverted sample exponent: `(d+2 beta)/beta`
- `d=48, beta=2` sample exponent: `{claim5_result['comparison']['prior_sample_exponent']}`
- Independent checker: `{claim5_checker['status']}`
- Mutated-evidence checker exit: `{claim5_control.returncode}` (nonzero required)
- Git SHA: `{claim5_result['environment']['git_sha']}`
- Runtime: `{claim5_result['environment']['runtime_seconds']:.6f}` seconds
- Allocation: `{claim5_result['environment']['cpu_limit']}` vCPU, `{claim5_result['environment']['memory_limit_bytes']}` bytes RAM, no accelerator

The pinned Cai-Li source states a beta-Holder assumption and derives the TV
rate through score-error, convergence, early-stopping, and triangle-inequality
steps. Exact exponent arithmetic independently yields the displayed sample
complexity and its increasing ambient-dimension exponent. Zhang et al. provide
an independent matching TV rate under beta-Sobolev, not beta-Holder, smoothness.

The certificate corrects one transparent missing `n^(-1/2)` factor in a Cai-Li
intermediate simplified display by deriving the exponent from its immediately
preceding unsimplified expression. It does not independently re-prove every
analytic lemma in either primary paper, which limits confidence to MEDIUM.
"""
(claim5_out / "EVAL.md").write_text(claim5_evaluation)
print(claim5_evaluation)
