import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_live_contract_is_five_claims():
    claims = json.loads((ROOT / 'contract/live_claims.json').read_text())
    assert len(claims) == 5
    assert all(item['status'] == 'unverified' for item in claims)

def test_source_hash_manifest_matches():
    for line in (ROOT / 'evidence/source/SHA256SUMS').read_text().splitlines():
        digest, name = line.split(maxsplit=1)
        path = ROOT / name.strip()
        assert path.exists()
        assert hashlib.sha256(path.read_bytes()).hexdigest() == digest
