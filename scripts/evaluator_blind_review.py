#!/usr/bin/env python3
"""Fail-closed review using only a freshly assembled Space candidate."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import tempfile
import time
import urllib.parse
import urllib.request
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
SPACE_ID = "DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions"
PROTECTED_REVISION = "fe1fd273934cf8568fbcc1187d857e7662313648"
MANIFEST = ROOT / ".openresearch/artifacts/baseline/judged_space_manifest.sha256"
BLOB_PREFIX = f"https://huggingface.co/spaces/{SPACE_ID}/blob/main/"
USER_AGENT = "Mozilla/5.0 OpenResearch-evaluator-blind-review/1.0"
TEXT_SUFFIXES = {".json", ".lock", ".md", ".py", ".sh", ".toml", ".txt"}
REQUIRED_LINK_FILES = {
    "claim_contract.json",
    "source_audit.md",
    "method.md",
    "raw_results.json",
    "independent_checker.json",
    "negative_control_output.json",
    "reproduction.md",
    "resource_estimate.md",
    "EVAL.md",
    "limitations.md",
}


def safe_relative_path(value: str) -> Path:
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or not path.parts:
        raise ValueError(f"unsafe candidate path: {value!r}")
    return Path(*path.parts)


def protected_entries() -> list[tuple[str, str]]:
    entries = []
    for line in MANIFEST.read_text().splitlines():
        if not line.strip():
            continue
        digest, relative = line.split(maxsplit=1)
        entries.append((digest, relative.strip()))
    return entries


def download_protected_file(relative: str) -> bytes:
    quoted = urllib.parse.quote(relative, safe="/")
    url = f"https://huggingface.co/spaces/{SPACE_ID}/resolve/{PROTECTED_REVISION}/{quoted}"
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=45) as response:
                return response.read()
        except Exception as error:
            last_error = error
            if attempt < 2:
                time.sleep(1)
    raise RuntimeError(f"could not download protected file {relative}: {last_error}")


def draft_overlay_paths() -> list[str]:
    paths = {
        "README.md",
        "logbook.json",
        "reproduction_verdicts.json",
        "pyproject.toml",
        "uv.lock",
        "scripts/bootstrap_reproduction.sh",
        "scripts/evaluator_blind_review.py",
        "scripts/report_environment.py",
        "scripts/run_full_poster_gates.sh",
        "scripts/run_research_checks.py",
        "scripts/validate_release.py",
    }
    for pattern in (
        "pages/current-*/page.md",
        "pages/historical-claim-1-euler/page.md",
        ".openresearch/artifacts/claim*/**/*",
        "src/claim*.py",
        "verifiers/verify_claim*.py",
    ):
        paths.update(
            item.relative_to(ROOT).as_posix()
            for item in ROOT.glob(pattern)
            if item.is_file()
        )
    return sorted(paths)


def committed_bytes(relative: str) -> bytes:
    completed = subprocess.run(
        ["git", "show", f"HEAD:{relative}"],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
    )
    return completed.stdout


def release_overlay_paths() -> list[str]:
    allowlist = ROOT / "release/HF_TEXT_ALLOWLIST.txt"
    if not allowlist.exists():
        return draft_overlay_paths()
    paths = [
        line.strip()
        for line in committed_bytes("release/HF_TEXT_ALLOWLIST.txt").decode().splitlines()
        if line.strip()
    ]
    if paths != sorted(set(paths)):
        raise ValueError("release allowlist must be sorted and unique")
    return paths


def assemble_candidate(directory: Path, overlay_paths: list[str]) -> tuple[dict, dict]:
    protected = protected_entries()
    protected_paths = {relative for _, relative in protected}
    mutable_protected_paths = {"README.md", "logbook.json"}
    forbidden_overlaps = protected_paths.intersection(overlay_paths) - mutable_protected_paths
    if forbidden_overlaps:
        raise ValueError(
            "candidate overlay would modify protected historical files: "
            + ", ".join(sorted(forbidden_overlaps))
        )
    for expected, relative in protected:
        data = download_protected_file(relative)
        actual = hashlib.sha256(data).hexdigest()
        if actual != expected:
            raise ValueError(f"protected hash mismatch for {relative}: {actual}")
        destination = directory / safe_relative_path(relative)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)

    protected_book = json.loads((directory / "logbook.json").read_text())
    for relative in overlay_paths:
        source = ROOT / safe_relative_path(relative)
        if not source.is_file():
            raise FileNotFoundError(f"allowlisted file is absent: {relative}")
        if source.suffix not in TEXT_SUFFIXES and source.name not in {"README.md", "uv.lock"}:
            raise ValueError(f"non-text upload path: {relative}")
        data = committed_bytes(relative)
        data.decode("utf-8")
        destination = directory / safe_relative_path(relative)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)

    candidate_book = json.loads((directory / "logbook.json").read_text())
    return protected_book, candidate_book


def flatten_nodes(node: dict) -> list[dict]:
    result = [node]
    for child in node.get("children", []):
        result.extend(flatten_nodes(child))
    return result


class BlindReviewer:
    def __init__(self, candidate: Path, protected_book: dict, candidate_book: dict):
        self.candidate = candidate
        self.protected_book = protected_book
        self.candidate_book = candidate_book
        self.opened: list[str] = []
        self.release_gate_files: list[str] = []
        self.issues: list[dict[str, str]] = []

    def issue(self, code: str, detail: str) -> None:
        self.issues.append({"code": code, "detail": detail})

    def open_bytes(self, relative: str) -> bytes:
        relative = safe_relative_path(relative).as_posix()
        target = self.candidate / relative
        if relative not in self.opened:
            self.opened.append(relative)
        if not target.is_file():
            self.issue("missing_file", relative)
            return b""
        return target.read_bytes()

    def open_text(self, relative: str) -> str:
        data = self.open_bytes(relative)
        try:
            return data.decode("utf-8")
        except UnicodeDecodeError:
            self.issue("non_text_link", relative)
            return ""

    def gate_bytes(self, relative: str) -> bytes:
        relative = safe_relative_path(relative).as_posix()
        if relative not in self.release_gate_files:
            self.release_gate_files.append(relative)
        target = self.candidate / relative
        if not target.is_file():
            self.issue("missing_file", relative)
            return b""
        return target.read_bytes()

    def gate_text(self, relative: str) -> str:
        data = self.gate_bytes(relative)
        try:
            return data.decode("utf-8")
        except UnicodeDecodeError:
            self.issue("release.non_text", relative)
            return ""

    def linked_candidate_paths(self, page: str) -> list[str]:
        paths = []
        for link in re.findall(r"\((https://[^)]+)\)", page):
            if link.startswith(BLOB_PREFIX):
                paths.append(urllib.parse.unquote(link[len(BLOB_PREFIX) :]))
        return sorted(set(paths))

    def review_claim_page(self, claim_number: int, relative: str) -> None:
        page = self.open_text(relative)
        verdict = re.search(r"^## Reviewer verdict: (VERIFIED|FALSIFIED|BLOCKED)$", page, re.MULTILINE)
        if not verdict:
            self.issue("claim.verdict", f"Claim {claim_number}: exact verdict missing")
        if not re.search(r"\b(HIGH|MEDIUM|LOW)\b", page):
            self.issue("claim.confidence", f"Claim {claim_number}: confidence missing")

        required_phrases = {
            "claim.contract_inline": "Exact claim contract",
            "claim.source": "ar5iv.labs.arxiv.org",
            "claim.quantifiers": "Assumption",
            "claim.checker": "checker",
            "claim.control": "control",
            "claim.command": "Fixed inherited command",
            "claim.environment": "Locked environment",
            "claim.cpu": "cpu-upgrade",
            "claim.accelerator": "no accelerator",
            "claim.runtime": "seconds",
            "claim.git": "Git SHA",
            "claim.seed": "seed",
            "claim.limitations": "## Limitations",
            "claim.visibility": "## Evaluator visibility",
        }
        lower_page = page.lower()
        for code, phrase in required_phrases.items():
            if phrase.lower() not in lower_page:
                self.issue(code, f"Claim {claim_number}: {phrase!r} not visible")
        scientific_page = page.split("## Evaluator visibility", 1)[0]
        if not re.search(r"^\|[^\n]*\d", scientific_page, re.MULTILINE):
            self.issue("claim.raw_inline", f"Claim {claim_number}: raw numerical data is not inline")

        linked_paths = self.linked_candidate_paths(page)
        for linked in linked_paths:
            self.open_bytes(linked)
        linked_names = {PurePosixPath(path).name for path in linked_paths}
        for required in sorted(REQUIRED_LINK_FILES - linked_names):
            self.issue("claim.link", f"Claim {claim_number}: {required} is not directly linked")
        if not any(path.startswith("src/") for path in linked_paths):
            self.issue("claim.code", f"Claim {claim_number}: generator source is not directly linked")
        if not any(path.startswith("verifiers/") for path in linked_paths):
            self.issue("claim.verifier", f"Claim {claim_number}: verifier source is not directly linked")

        for suffix, code in (
            ("raw_results.json", "claim.raw_json"),
            ("independent_checker.json", "claim.checker_json"),
            ("negative_control_output.json", "claim.control_json"),
        ):
            matches = [path for path in linked_paths if path.endswith(suffix)]
            if not matches:
                continue
            try:
                payload = json.loads(self.open_text(matches[0]))
            except json.JSONDecodeError as error:
                self.issue(code, f"Claim {claim_number}: invalid JSON: {error}")
                continue
            if suffix == "independent_checker.json" and payload.get("status") != "PASS":
                self.issue(code, f"Claim {claim_number}: checker status is not PASS")
            if suffix == "negative_control_output.json":
                if payload.get("actual_exit_code", 0) == 0 or payload.get("passed") is not True:
                    self.issue(code, f"Claim {claim_number}: negative control did not fail as required")

    def review_manifest(self) -> None:
        allowlist_path = self.candidate / "release/HF_TEXT_ALLOWLIST.txt"
        manifest_path = self.candidate / "release/HF_TEXT_MANIFEST.sha256"
        if not allowlist_path.is_file():
            self.issue("release.allowlist", "exact HF text allowlist is missing")
            return
        if not manifest_path.is_file():
            self.issue("release.manifest", "SHA-256 upload manifest is missing")
            return
        allowlist = [line.strip() for line in self.gate_text("release/HF_TEXT_ALLOWLIST.txt").splitlines() if line.strip()]
        manifest = {}
        for line in self.gate_text("release/HF_TEXT_MANIFEST.sha256").splitlines():
            if not line.strip():
                continue
            digest, relative = line.split(maxsplit=1)
            manifest[relative.strip()] = digest
        expected_manifest_paths = set(allowlist) - {"release/HF_TEXT_MANIFEST.sha256"}
        if set(manifest) != expected_manifest_paths:
            self.issue("release.manifest_paths", "manifest paths do not exactly match the allowlist")
        for relative, expected in manifest.items():
            actual = hashlib.sha256(self.gate_bytes(relative)).hexdigest()
            if actual != expected:
                self.issue("release.manifest_hash", f"hash mismatch: {relative}")

    def review_secrets(self, overlay_paths: list[str]) -> None:
        patterns = {
            "hf_token": re.compile(rb"hf_[A-Za-z0-9]{20,}"),
            "github_token": re.compile(rb"(?:ghp|github_pat)_[A-Za-z0-9_]{20,}"),
            "private_key": re.compile(rb"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
            "aws_key": re.compile(rb"AKIA[0-9A-Z]{16}"),
        }
        for relative in overlay_paths:
            data = self.gate_bytes(relative)
            for name, pattern in patterns.items():
                if pattern.search(data):
                    self.issue("release.secret", f"{name} pattern found in {relative}")

    def run(self, overlay_paths: list[str]) -> dict:
        readme = self.open_text("README.md")
        if "sdk: static" not in readme or "logbook.json" not in readme or "canonical" not in readme.lower():
            self.issue("entrypoint.readme", "README does not identify logbook.json as the canonical evaluator entrypoint")

        self.open_text("logbook.json")
        protected_nodes = {(node["slug"], node["file"]) for node in flatten_nodes(self.protected_book["root"])}
        candidate_nodes = {(node["slug"], node["file"]) for node in flatten_nodes(self.candidate_book["root"])}
        if not protected_nodes <= candidate_nodes:
            self.issue("history.page_tree", "protected page-tree nodes are not a subset of the candidate")
        protected_paths = {relative for _, relative in protected_entries()}
        candidate_paths = {
            item.relative_to(self.candidate).as_posix()
            for item in self.candidate.rglob("*")
            if item.is_file()
        }
        if not protected_paths <= candidate_paths:
            self.issue("history.file_tree", "protected Space files are not a subset of the candidate")

        root = self.candidate_book["root"]
        current_children = [node for node in root.get("children", []) if node.get("title", "").startswith("Current Claim ")]
        if len(current_children) != 5:
            self.issue("navigation.current_claims", f"expected 5 current claim pages, found {len(current_children)}")
        historical = [node for node in root.get("children", []) if node.get("title") == "Historical rejected baseline"]
        if len(historical) != 1 or root.get("children", [])[-1].get("title") != "Historical rejected baseline":
            self.issue("navigation.history", "historical baseline is not the final top-level node")

        for node in flatten_nodes(root):
            self.open_text(node["file"])
        root_page = self.open_text(root["file"])
        matrix_header = "| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |"
        if matrix_header not in root_page:
            self.issue("visibility.matrix", "canonical visibility matrix is missing")

        for claim_number, node in enumerate(current_children, start=1):
            self.review_claim_page(claim_number, node["file"])

        self.review_manifest()
        self.review_secrets(overlay_paths)
        return {
            "status": "PASS" if not self.issues else "FAIL",
            "space_id": SPACE_ID,
            "protected_revision": PROTECTED_REVISION,
            "candidate_source": "fresh protected download plus repository text overlay",
            "reviewer_opened_files": self.opened,
            "release_gate_files": self.release_gate_files,
            "issues": self.issues,
            "visibility_rows_complete": not any(issue["code"].startswith(("claim.", "visibility.")) for issue in self.issues),
            "protected_file_subset": not any(issue["code"] == "history.file_tree" for issue in self.issues),
            "protected_page_subset": not any(issue["code"] == "history.page_tree" for issue in self.issues),
        }


def main() -> int:
    overlay_paths = release_overlay_paths()
    with tempfile.TemporaryDirectory(prefix="l5jtapudbq-candidate-") as temporary:
        candidate = Path(temporary)
        protected_book, candidate_book = assemble_candidate(candidate, overlay_paths)
        result = BlindReviewer(candidate, protected_book, candidate_book).run(overlay_paths)
    print("# Evaluator-blind candidate review")
    print(json.dumps(result, indent=2, sort_keys=True))
    print("EVALUATOR_REVIEW_JSON=" + json.dumps(result, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
