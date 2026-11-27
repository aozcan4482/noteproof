# NOTEPROOF-FILE
# module:   core
# owner:    arda            second: burak
# story:    -
# contract: 02#3, 02#5.1
# depends:  core.ns
# status:   stable
"""core/ns.py testleri: IRI'ler 02 bölüm 3'teki şemayı birebir üretir, geçersiz girdi reddedilir."""

from __future__ import annotations

import pytest

from core.ns import (
    NAMESPACE,
    account_iri,
    concept_iri,
    note_iri,
    proof_iri,
    registration_iri,
    timestamp_iri,
)

HASH = "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
NS = "https://github.com/aozcan4482/noteproof/ns#"


def test_namespace_is_the_k001_value():
    # anchor/proof.py (Burak) proof dosyalarında aynı değeri kullanır; değişirse proof'lar tutmaz.
    assert NAMESPACE == NS


@pytest.mark.parametrize(
    ("make", "expected"),
    [
        (note_iri, f"{NS}note/{HASH}"),
        (registration_iri, f"{NS}registration/{HASH}"),
        (proof_iri, f"{NS}proof/{HASH}"),
        (timestamp_iri, f"{NS}timestamp/{HASH}"),
    ],
)
def test_hash_based_iris_follow_the_scheme(make, expected):
    assert make(HASH) == expected


@pytest.mark.parametrize("make", [note_iri, registration_iri, proof_iri, timestamp_iri])
@pytest.mark.parametrize(
    "bad",
    ["", HASH.upper(), HASH[:-1], HASH + "0", "g" * 64, f" {HASH}", None],
)
def test_hash_based_iris_reject_invalid_hashes(make, bad):
    with pytest.raises(ValueError):
        make(bad)


def test_account_iri_uses_the_pseudonym():
    assert account_iri("mavi-kalem") == f"{NS}account/mavi-kalem"


def test_account_iri_escapes_characters_that_would_break_the_iri():
    iri = account_iri("a/b#c d")
    assert iri == f"{NS}account/a%2Fb%23c%20d"
    assert iri.count("#") == 1  # yalnızca namespace'teki


@pytest.mark.parametrize("bad", ["", "   ", None])
def test_account_iri_rejects_empty_pseudonym(bad):
    with pytest.raises(ValueError):
        account_iri(bad)


@pytest.mark.parametrize(
    ("local_id", "expected"),
    [
        ("Course_SEN0401", f"{NS}Course_SEN0401"),
        ("Topic_TransactionFees", f"{NS}Topic_TransactionFees"),
        ("Topic_FeeRate", f"{NS}Topic_FeeRate"),
    ],
)
def test_concept_iri_follows_the_scheme(local_id, expected):
    assert concept_iri(local_id) == expected


@pytest.mark.parametrize(
    "bad",
    ["", "Transaction fees", "Topic_", "Topic_Fee Rate", "Topic_Fee/Rate", "np:Topic_FeeRate", f"{NS}Topic_FeeRate",
     "CourseScheme", None],
)
def test_concept_iri_rejects_labels_and_full_iris(bad):
    # 02 bölüm 3: API'de yerel kimlik geçer, etiket metniyle eşleştirme yapılmaz.
    with pytest.raises(ValueError):
        concept_iri(bad)
