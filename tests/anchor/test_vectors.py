# NOTEPROOF-FILE
# module:   anchor
# owner:    burak           second: arda
# story:    S2, S7
# contract: 02#5.5 Merkle kuralları, 02#6 proof dosyası
# depends:  -
# status:   wip
"""tests/vectors/ testleri (BRK-3).

Aynı vektör dosyalarını Erdener'in tarayıcı testi (`tests/web/`) de okuyacak. Bu testler Python tarafının
vektörlerle uyuştuğunu ve dosyaların `python -m anchor.vectors` çıktısıyla birebir aynı olduğunu gösterir.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from anchor import merkle, proof, vectors
from anchor.merkle import PathStep

VECTORS_DIR = Path(__file__).resolve().parents[1] / "vectors"
EXPECTED_PROOF_FIELDS = {
    # NP-CONTRACT(02#6): proof dosyasının alanları sabit
    "@context", "@type", "@id", "noteHash", "hashAlgorithm", "leafPrefix", "nodePrefix",
    "merklePath", "merkleRoot", "network", "txid", "blockHeight", "blockHash", "blockTime",
}


def load(name: str) -> dict:
    return json.loads((VECTORS_DIR / name).read_text(encoding="utf-8"))


def path_of(steps: list[dict]) -> list[PathStep]:
    return [PathStep(s["side"], bytes.fromhex(s["sibling"])) for s in steps]


def test_s7_vector_files_match_generator():
    # Dosyalar elle değiştirilmemiş olmalı; değişirse `python -m anchor.vectors` ile yeniden üretilir.
    for name, content in vectors.render().items():
        assert (VECTORS_DIR / name).read_bytes() == content, f"{name} üretilen çıktıyla aynı değil"


def test_s7_vectors_use_the_fixed_merkle_rules():
    data = load("merkle_vectors.json")
    assert data["hashAlgorithm"] == "SHA-256"
    assert data["leafPrefix"] == "00" and data["nodePrefix"] == "01"
    assert [t["leafCount"] for t in data["trees"]] == [1, 2, 3, 5, 8]


def test_s7_every_vector_path_verifies():
    data = load("merkle_vectors.json")
    for tree in data["trees"]:
        root = bytes.fromhex(tree["merkleRoot"])
        assert len(tree["proofs"]) == tree["leafCount"]
        for case in tree["proofs"]:
            ok = merkle.verify_path(bytes.fromhex(case["noteHash"]), path_of(case["merklePath"]), root)
            assert ok is case["expected"] is True


@pytest.mark.parametrize("case", load("merkle_vectors.json")["negative"], ids=lambda c: c["name"])
def test_s7_bad_vectors_are_rejected(case):
    ok = merkle.verify_path(
        bytes.fromhex(case["noteHash"]), path_of(case["merklePath"]), bytes.fromhex(case["merkleRoot"])
    )
    assert ok is case["expected"] is False


def test_s7_negative_kinds_cover_tampered_path_wrong_root_and_wrong_side():
    names = {c["name"].rsplit("-", 1)[0] for c in load("merkle_vectors.json")["negative"]}
    assert names == {"wrong-root", "tampered-sibling", "wrong-side"}


def test_s7_sample_proof_has_exactly_the_contract_fields():
    assert set(load("sample_proof.json")) == EXPECTED_PROOF_FIELDS


def test_s7_sample_note_verifies_offline():
    note = (VECTORS_DIR / "sample_note.txt").read_bytes()
    ok, message = proof.verify_offline(load("sample_proof.json"), note)
    assert ok, message


def test_s7_rejection_changed_sample_note_is_not_the_registered_file():
    # 01 bölüm 7'deki zorunlu reddetme senaryosu: tek karakteri değişen dosya kayıtlı dosya değildir.
    note = (VECTORS_DIR / "sample_note.txt").read_bytes()
    tampered = note.replace(b"RBF", b"RBX", 1)
    assert tampered != note
    ok, message = proof.verify_offline(load("sample_proof.json"), tampered)
    assert not ok and "kayıtlı dosya değil" in message


def test_s7_sample_note_has_no_windows_line_endings():
    # .gitattributes (tests/vectors/* -text) bunu korur; CRLF olsaydı hash değişirdi.
    assert b"\r\n" not in (VECTORS_DIR / "sample_note.txt").read_bytes()
