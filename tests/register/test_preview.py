# NOTEPROOF-FILE
# module:   register
# owner:    arda            second: burak
# story:    S1, S3, S6
# contract: 02#7 POST /api/notes/preview; K-006
# depends:  register.app.app
# status:   wip
"""Önizleme testleri (ARD-3).

Kabul ölçütü: yanıt 02 bölüm 7'deki önizleme biçiminde; çağrıdan sonra grafikte ve data/ altında hiçbir
kalıcı kayıt yok; kayıtlı hash için alreadyRegistered dolu. Dil modeli yerine FakeLLM kullanılır, ağa çıkılmaz.
"""

from __future__ import annotations

import io
import json

import pytest

from copywarn import RegisteredNote
from core.hashing import sha256_hex
from core.ns import account_iri, note_iri, registration_iri
from register import state
from register.app import app
from register.preview import PreviewCache, PreviewEntry

from .conftest import assert_error

NOTE = (
    "İşlem ücretleri (transaction fees) madencilere ödenir. Ücret oranı sat/vB ile ölçülür ve yüksek ücretli "
    "işlemler bloğa önce girer. Mempool doluyken düşük ücretli işlemler bekler."
).encode("utf-8")
S3_ANSWER = json.dumps({
    "course": "Course_SEN0401",
    "topics": ["Topic_TransactionFees", "Topic_Uydurma"],
    "summary": "Not işlem ücretlerini anlatır. Ücret oranının bloğa girişi etkilediğini açıklar.",
})


class FakeLLM:
    """Ağa çıkmayan dil modeli (03 bölüm 8); tagger.llm.LLMClient arayüzüne uyar."""

    def __init__(self, answer: str) -> None:
        self.answer = answer
        self.calls = 0

    def complete(self, prompt: str, *, system: str | None = None) -> str:
        self.calls += 1
        return self.answer


@pytest.fixture
def llm():
    fake = FakeLLM(S3_ANSWER)
    app.dependency_overrides[state.llm_client] = lambda: fake
    yield fake
    app.dependency_overrides.pop(state.llm_client, None)


@pytest.fixture
def token(client):
    return client.post("/api/accounts", json={"pseudonym": "mavi_kalem"}).json()["token"]


def _preview(client, token, data=NOTE, name="not.txt", content_type="text/plain"):
    headers = {"X-NoteProof-Token": token} if token else {}
    return client.post("/api/notes/preview", files={"file": (name, io.BytesIO(data), content_type)}, headers=headers)


def _snapshot(folder):
    # graph/ hariç: Oxigraph'ın altındaki RocksDB iç dosyalarını yazma olmadan da arka planda yeniden düzenler.
    # Grafiğin içeriği ayrıca üçlü sayısıyla denetlenir.
    return sorted(
        (str(p.relative_to(folder)), p.stat().st_size)
        for p in folder.rglob("*")
        if p.is_file() and p.relative_to(folder).parts[0] != "graph"
    )


# --- Kabul ölçütleri -----------------------------------------------------------------------------------

def test_s3_acceptance_transaction_fee_note_gets_course_and_topic(client, token, llm):
    response = _preview(client, token)
    assert response.status_code == 200, response.text
    body = response.json()
    assert set(body) == {"previewToken", "noteHash", "alreadyRegistered", "suggestion", "copyWarnings"}
    assert body["noteHash"] == sha256_hex(NOTE)
    assert body["alreadyRegistered"] is None
    assert body["suggestion"]["course"] == "Course_SEN0401"
    assert body["suggestion"]["topics"] == ["Topic_TransactionFees"]  # sözlükte olmayan konu süzüldü
    assert body["suggestion"]["summary"]
    assert body["copyWarnings"] == []
    assert llm.calls == 1


def test_s3_acceptance_preview_saves_nothing(client, token, llm, data_dir):
    # "Onaya kadar hiçbir şey kaydedilmez" (S3, G4): grafik ve data/ önizlemeden önceki hâlinde kalır.
    graph = state.graph_store()
    quads_before = len(list(graph.quads_for_pattern(None, None, None)))
    files_before = _snapshot(data_dir)

    assert _preview(client, token).status_code == 200

    assert len(list(graph.quads_for_pattern(None, None, None))) == quads_before
    assert _snapshot(data_dir) == files_before
    for folder in ("notes", "text", "proofs"):
        assert not (data_dir / folder).exists()
    assert len(state.copy_checker()._notes) == 0  # kopya havuzuna da eklenmedi


def test_already_registered_hash_returns_earlier_record(client, token, llm):
    # ARD-4'ün yazacağı üçlüler elle konur: başka bir hesabın aynı dosyayı önceden kaydettiği durum.
    import pyoxigraph

    other = client.post("/api/accounts", json={"pseudonym": "kuzgun"}).json()["account"]
    note_hash = sha256_hex(NOTE)
    prov = "http://www.w3.org/ns/prov#"
    note, reg = pyoxigraph.NamedNode(note_iri(note_hash)), pyoxigraph.NamedNode(registration_iri(note_hash))
    state.graph_store().extend([
        pyoxigraph.Quad(note, pyoxigraph.NamedNode(prov + "wasGeneratedBy"), reg),
        pyoxigraph.Quad(note, pyoxigraph.NamedNode(prov + "wasAttributedTo"), pyoxigraph.NamedNode(other)),
        pyoxigraph.Quad(reg, pyoxigraph.NamedNode(prov + "endedAtTime"), pyoxigraph.Literal(
            "2026-11-18T11:05:00+00:00", datatype=pyoxigraph.NamedNode("http://www.w3.org/2001/XMLSchema#dateTime"))),
    ])

    body = _preview(client, token).json()
    assert body["alreadyRegistered"] == {
        "registeredAt": "2026-11-18T11:05:00Z",  # Oxigraph xsd:dateTime'ı Z ile normalize eder; ikisi de UTC
        "author": "kuzgun",
        "proofUrl": f"/api/notes/{note_hash}/proof",
    }
    assert body["suggestion"] is None
    assert body["copyWarnings"] == []
    assert llm.calls == 0  # kayıtlı dosya için dil modeli çağrılmaz


def test_s6_similar_earlier_note_of_another_author_gives_possible_copy_warning(client, token, llm):
    earlier_hash = "7c1a60358b1eec6b402a1fbcb8cf3961cefb793d82c7f37006d46c5121156950"
    state.copy_checker().add(RegisteredNote(earlier_hash, NOTE.decode(), "kuzgun", "2026-11-18T11:05:00+00:00"))

    warnings = _preview(client, token).json()["copyWarnings"]
    assert len(warnings) == 1
    w = warnings[0]
    assert set(w) == {"earlierNoteHash", "earlierAuthor", "earlierRegisteredAt", "earlierProofUrl", "score", "method"}
    assert w["earlierNoteHash"] == earlier_hash
    assert w["earlierAuthor"] == "kuzgun"
    assert w["earlierProofUrl"] == f"/api/notes/{earlier_hash}/proof"
    assert w["score"] >= 0.6


def test_own_earlier_note_is_not_a_copy(client, token, llm):
    state.copy_checker().add(RegisteredNote("a" * 64, NOTE.decode(), "mavi_kalem", "2026-11-18T11:05:00+00:00"))
    assert _preview(client, token).json()["copyWarnings"] == []


# --- Tür, boyut, kimlik ---------------------------------------------------------------------------------

def test_preview_needs_a_token(client, llm):
    assert_error(_preview(client, None), 401, "unauthorized")
    assert_error(_preview(client, "yanlis"), 401, "unauthorized")


@pytest.mark.parametrize(("name", "content_type"), [
    ("not.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
    ("not.zip", "application/zip"),
    ("not.exe", "application/octet-stream"),
])
def test_unsupported_type_is_400(client, token, llm, name, content_type):
    assert_error(_preview(client, token, b"PK\x03\x04...", name, content_type), 400, "unsupported_type")


def test_content_that_does_not_match_the_type_is_400(client, token, llm):
    assert_error(_preview(client, token, b"bu bir PDF degil", "not.pdf", "application/pdf"), 400, "unsupported_type")


def test_markdown_without_content_type_is_detected_from_extension(client, token, llm):
    assert _preview(client, token, NOTE, "not.md", "application/octet-stream").status_code == 200


def test_non_utf8_text_is_400(client, token, llm):
    assert_error(_preview(client, token, "Işık".encode("cp1254")), 400, "unsupported_type")


def test_file_over_10_mb_is_400_too_large(client, token, llm):
    assert_error(_preview(client, token, b"a" * (10 * 1024 * 1024 + 1)), 400, "too_large")


def test_file_of_exactly_10_mb_is_accepted(client, token, llm):
    assert _preview(client, token, b"a " * (5 * 1024 * 1024)).status_code == 200


def test_empty_file_is_422(client, token, llm):
    assert_error(_preview(client, token, b""), 422, "invalid_request")


# --- Önerinin olmadığı durumlar: önizleme yine de çalışır, yazar elle seçer -------------------------------

def test_without_llm_configuration_suggestion_is_empty(client, token, monkeypatch):
    for name in ("NOTEPROOF_LLM_PROVIDER", "NOTEPROOF_LLM_MODEL", "NOTEPROOF_LLM_API_KEY"):
        monkeypatch.delenv(name, raising=False)
    state.llm_client.cache_clear()
    body = _preview(client, token).json()
    assert body["suggestion"] == {"course": None, "topics": [], "summary": ""}


def test_pdf_without_text_gives_empty_suggestion(client, token, llm):
    pypdf = pytest.importorskip("pypdf")
    out = io.BytesIO()
    writer = pypdf.PdfWriter()
    writer.add_blank_page(width=200, height=200)
    writer.write(out)
    body = _preview(client, token, out.getvalue(), "bos.pdf", "application/pdf").json()
    assert body["suggestion"] == {"course": None, "topics": [], "summary": ""}
    assert llm.calls == 0


def test_llm_failure_does_not_break_preview(client, token):
    class BrokenLLM:
        def complete(self, prompt, *, system=None):
            raise ConnectionError("ağ yok")

    app.dependency_overrides[state.llm_client] = lambda: BrokenLLM()
    try:
        body = _preview(client, token).json()
    finally:
        app.dependency_overrides.pop(state.llm_client, None)
    assert body["suggestion"] == {"course": None, "topics": [], "summary": ""}


# --- Bellekteki önizlemeler ---------------------------------------------------------------------------

def test_preview_is_kept_in_memory_for_the_same_account(client, token, llm):
    body = _preview(client, token).json()
    account = account_iri("mavi_kalem")
    entry = state.preview_cache().get(body["previewToken"], account)
    assert entry is not None and entry.note_hash == body["noteHash"] and entry.data == NOTE
    assert state.preview_cache().get(body["previewToken"], account.replace("mavi_kalem", "kuzgun")) is None


def _entry(token: str) -> PreviewEntry:
    return PreviewEntry(token, "acc", "h", b"", "text/plain", "", "", None, [], None)


def test_preview_cache_expires_after_ttl():
    now = [0.0]
    cache = PreviewCache(ttl=900, clock=lambda: now[0])
    cache.put(_entry("t1"))
    now[0] = 899
    assert cache.get("t1", "acc") is not None
    now[0] = 900
    assert cache.get("t1", "acc") is None


def test_preview_cache_drops_the_oldest_when_full():
    cache = PreviewCache(max_entries=2)
    for t in ("t1", "t2", "t3"):
        cache.put(_entry(t))
    assert cache.get("t1", "acc") is None
    assert cache.get("t3", "acc") is not None
    assert len(cache) == 2
