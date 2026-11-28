# NOTEPROOF-FILE
# module:   register
# owner:    arda            second: burak
# story:    S1, S4, S6
# contract: 02#7 POST /api/notes
# depends:  register.app.app, shapes.validate.validate_note, anchor.store.Store
# status:   wip
"""Kayıt testleri (ARD-4).

Kabul ölçütü: S1 kabul testi; sözlükte olmayan konu → 422 shape_violation ve grafikte kayıt yok (S4);
confirmed yoksa 400; başarılı kayıttan sonra hash kuyrukta.
"""

from __future__ import annotations

import io
import re

import pytest
import rdflib

from core.hashing import sha256_hex
from core.ns import NAMESPACE, note_iri
from register import state
from register.app import app
from shapes.validate import validate_note

from .conftest import assert_error
from .test_preview import NOTE, FakeLLM, S3_ANSWER


@pytest.fixture(autouse=True)
def llm():
    app.dependency_overrides[state.llm_client] = lambda: FakeLLM(S3_ANSWER)
    yield
    app.dependency_overrides.pop(state.llm_client, None)


def _account(client, pseudonym="mavi_kalem") -> str:
    return client.post("/api/accounts", json={"pseudonym": pseudonym}).json()["token"]


def _preview(client, token, data=NOTE) -> dict:
    files = {"file": ("not.txt", io.BytesIO(data), "text/plain")}
    response = client.post("/api/notes/preview", files=files, headers={"X-NoteProof-Token": token})
    assert response.status_code == 200, response.text
    return response.json()


def _confirm(client, token, preview_token, **overrides):
    body = {
        "previewToken": preview_token,
        "title": "İşlem ücretleri",
        "course": "Course_SEN0401",
        "topics": ["Topic_TransactionFees"],
        "summary": "Not işlem ücretlerini anlatır. Ücret oranının bloğa girişi etkilediğini açıklar.",
        "confirmed": True,
    }
    body.update(overrides)
    return client.post("/api/notes", json=body, headers={"X-NoteProof-Token": token})


def _quads():
    return list(state.graph_store().quads_for_pattern(None, None, None))


def _note_graph(note_hash: str) -> rdflib.Graph:
    """Depodaki not ve kayıt üçlülerini rdflib grafiğine çevirir (shape'lerle yeniden denetlemek için)."""
    import pyoxigraph

    nt = state.graph_store().dump(format=pyoxigraph.RdfFormat.N_QUADS, from_graph=pyoxigraph.DefaultGraph())
    g = rdflib.Graph()
    g.parse(data=nt, format="nt")
    return g


def _in_queue(note_hash: str) -> bool:
    # Store.enqueue (02#5.5): False → bu hash zaten kuyrukta.
    queue = state.anchor_queue()()
    try:
        return queue.enqueue(note_hash) is False
    finally:
        queue.close()


# --- Kabul ölçütleri -----------------------------------------------------------------------------------

def test_s1_acceptance_register_gives_hash_time_and_pending_proof(client, data_dir):
    token = _account(client)
    preview = _preview(client, token)
    response = _confirm(client, token, preview["previewToken"])

    assert response.status_code == 201, response.text
    body = response.json()
    assert set(body) == {"noteHash", "registeredAt", "status", "proofStatus"}
    assert body["noteHash"] == sha256_hex(NOTE)
    assert re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", body["registeredAt"])
    assert body["status"] == "registered"
    assert body["proofStatus"] == "pending"

    # Hash kuyrukta: bir sonraki günlük timestamp onu Bitcoin işlemine bağlayacak.
    assert _in_queue(body["noteHash"])
    # Dosya ve metin data/ altında (02 bölüm 2).
    assert (data_dir / "notes" / f"{body['noteHash']}.txt").read_bytes() == NOTE
    assert (data_dir / "text" / f"{body['noteHash']}.txt").read_text(encoding="utf-8").strip()


def test_registered_note_conforms_to_the_shapes(client):
    # Definition of Done 2: notlar shape'lere uyar (kayıt servisinin testlerinde pySHACL).
    token = _account(client)
    note_hash = _confirm(client, token, _preview(client, token)["previewToken"]).json()["noteHash"]
    report = validate_note(_note_graph(note_hash))
    assert report.conforms, report.violations


def test_registered_note_has_prov_record_and_pseudonymous_author(client):
    token = _account(client)
    note_hash = _confirm(client, token, _preview(client, token)["previewToken"]).json()["noteHash"]
    g = _note_graph(note_hash)
    note = rdflib.URIRef(note_iri(note_hash))
    prov = rdflib.Namespace("http://www.w3.org/ns/prov#")
    np_ = rdflib.Namespace(NAMESPACE)

    account = g.value(note, prov.wasAttributedTo)
    assert str(account) == f"{NAMESPACE}account/mavi_kalem"
    registration = g.value(note, prov.wasGeneratedBy)
    assert g.value(registration, prov.wasAssociatedWith) == account
    assert g.value(registration, prov.endedAtTime) is not None
    assert str(g.value(note, np_.status)) == "registered"
    assert g.value(note, np_.tagsConfirmed).toPython() is True
    assert {str(t) for t in g.objects(note, np_.topic)} == {f"{NAMESPACE}Topic_TransactionFees"}


def test_s4_acceptance_topic_not_in_vocabulary_is_rejected_and_nothing_saved(client, data_dir):
    token = _account(client)
    preview = _preview(client, token)
    before = len(_quads())

    response = _confirm(client, token, preview["previewToken"], topics=["Topic_Uydurma"])

    assert_error(response, 422, "shape_violation")
    violations = response.json()["error"]["violations"]
    assert any(v["path"] == "np:topic" for v in violations)
    assert len(_quads()) == before
    assert not (data_dir / "notes").exists()
    assert not _in_queue(preview["noteHash"])


def test_s4_label_text_instead_of_id_is_rejected_the_same_way(client):
    token = _account(client)
    preview = _preview(client, token)
    response = _confirm(client, token, preview["previewToken"], topics=["Transaction fees"])
    assert_error(response, 422, "shape_violation")


def test_author_can_fix_tags_and_confirm_again_after_a_violation(client):
    token = _account(client)
    preview = _preview(client, token)
    assert _confirm(client, token, preview["previewToken"], topics=["Topic_Uydurma"]).status_code == 422
    assert _confirm(client, token, preview["previewToken"]).status_code == 201


def test_note_without_topics_is_rejected(client):
    token = _account(client)
    response = _confirm(client, token, _preview(client, token)["previewToken"], topics=[])
    assert_error(response, 422, "shape_violation")


@pytest.mark.parametrize("confirmed", [False, None, "true", 1, "missing"])
def test_not_confirmed_is_400_and_nothing_saved(client, confirmed):
    # Yalnızca JSON true onaydır: "true" metni, 1, null ya da alanın hiç olmaması onay sayılmaz (G4).
    token = _account(client)
    preview = _preview(client, token)
    before = len(_quads())
    body = {
        "previewToken": preview["previewToken"], "title": "t", "course": "Course_SEN0401",
        "topics": ["Topic_TransactionFees"], "summary": "",
    }
    if confirmed != "missing":
        body["confirmed"] = confirmed
    response = client.post("/api/notes", json=body, headers={"X-NoteProof-Token": token})
    assert_error(response, 400, "not_confirmed")
    assert len(_quads()) == before
    assert not _in_queue(preview["noteHash"])


# --- Önizleme ve kimlik ---------------------------------------------------------------------------------

def test_unknown_preview_token_is_410(client):
    assert_error(_confirm(client, _account(client), "bilinmeyen"), 410, "preview_expired")


def test_preview_of_another_account_cannot_be_confirmed(client):
    preview = _preview(client, _account(client, "mavi_kalem"))
    assert_error(_confirm(client, _account(client, "kuzgun"), preview["previewToken"]), 410, "preview_expired")


def test_preview_token_is_single_use(client):
    token = _account(client)
    preview = _preview(client, token)
    assert _confirm(client, token, preview["previewToken"]).status_code == 201
    assert_error(_confirm(client, token, preview["previewToken"]), 410, "preview_expired")


def test_register_needs_a_token(client):
    assert_error(_confirm(client, "yanlis", "x"), 401, "unauthorized")


def test_same_file_cannot_be_registered_twice(client):
    token = _account(client)
    assert _confirm(client, token, _preview(client, token)["previewToken"]).status_code == 201
    other = _account(client, "kuzgun")
    preview = _preview(client, other)
    assert preview["alreadyRegistered"]["author"] == "mavi_kalem"
    assert_error(_confirm(client, other, preview["previewToken"]), 409, "already_registered")


def test_empty_title_is_422(client):
    token = _account(client)
    assert_error(_confirm(client, token, _preview(client, token)["previewToken"], title="  "), 422, "invalid_request")


# --- Kopya uyarısı (S6) --------------------------------------------------------------------------------

def test_s6_acceptance_near_copy_of_earlier_note_is_marked_and_linked(client):
    first = _account(client, "kuzgun")
    earlier = _confirm(client, first, _preview(client, first)["previewToken"]).json()["noteHash"]

    later_text = NOTE.replace(b"madencilere", b"madencilere hemen")  # neredeyse aynı not
    second = _account(client, "mavi_kalem")
    preview = _preview(client, second, later_text)
    assert [w["earlierNoteHash"] for w in preview["copyWarnings"]] == [earlier]

    later = _confirm(client, second, preview["previewToken"]).json()["noteHash"]
    g = _note_graph(later)
    np_ = rdflib.Namespace(NAMESPACE)
    warning = rdflib.URIRef(f"{NAMESPACE}copywarning/{later}-{earlier}")
    assert (warning, rdflib.RDF.type, np_.CopyWarning) in g
    assert g.value(warning, np_.laterNote) == rdflib.URIRef(note_iri(later))
    assert g.value(warning, np_.earlierNote) == rdflib.URIRef(note_iri(earlier))
    assert float(g.value(warning, np_.score)) >= 0.6
    assert str(g.value(warning, np_.method))


# --- Yarıda kalan kayıt geri alınır ---------------------------------------------------------------------

def test_failure_while_queueing_rolls_back_graph_and_files(client, data_dir):
    class BrokenQueue:
        def enqueue(self, note_hash_hex, registered_at=None):
            raise OSError("disk dolu")

    token = _account(client)
    preview = _preview(client, token)
    before = len(_quads())
    app.dependency_overrides[state.anchor_queue] = lambda: BrokenQueue
    try:
        from fastapi.testclient import TestClient

        response = TestClient(app, raise_server_exceptions=False).post(
            "/api/notes", headers={"X-NoteProof-Token": token},
            json={"previewToken": preview["previewToken"], "title": "t", "course": "Course_SEN0401",
                  "topics": ["Topic_TransactionFees"], "summary": "", "confirmed": True},
        )
    finally:
        app.dependency_overrides.pop(state.anchor_queue, None)

    assert_error(response, 500, "internal_error")
    assert len(_quads()) == before
    assert not list((data_dir / "notes").glob("*"))
    assert not list((data_dir / "text").glob("*"))
