# NOTEPROOF-FILE
# module:   register
# owner:    arda            second: burak
# story:    S1
# contract: 02#7 POST /api/accounts, X-NoteProof-Token; K-007
# depends:  register.app.app
# status:   wip
"""Hesap ve token testleri (ARD-2).

Kabul ölçütü: token bir kez döner ve özetlenerek saklanır; geçersiz token → 401 unauthorized; hiçbir yerde
gerçek isim alanı yok.
"""

from __future__ import annotations

import sqlite3
from typing import Annotated

import pytest
from fastapi import Depends
from fastapi.routing import APIRoute

from core.hashing import sha256_hex
from core.ns import NAMESPACE
from register import state
from register.app import app, require_account

from .conftest import assert_error

ALT_NAME = "https://schema.org/alternateName"


def _create(client, pseudonym: str, **extra):
    return client.post("/api/accounts", json={"pseudonym": pseudonym, **extra})


def test_s1_create_account_returns_iri_and_token_once(client):
    response = _create(client, "mavi_kalem")
    assert response.status_code == 201
    body = response.json()
    assert set(body) == {"account", "token"}
    assert body["account"] == f"{NAMESPACE}account/mavi_kalem"
    assert len(body["token"]) >= 40


def test_pseudonym_is_lowercased(client):
    assert _create(client, "  Mavi-Kalem ").json()["account"] == f"{NAMESPACE}account/mavi-kalem"


def test_each_account_gets_a_different_token(client):
    assert _create(client, "aaa").json()["token"] != _create(client, "bbb").json()["token"]


def test_token_is_stored_only_as_a_hash(client, data_dir):
    token = _create(client, "mavi_kalem").json()["token"]
    raw = (data_dir / "accounts.sqlite").read_bytes()
    assert token.encode() not in raw
    with sqlite3.connect(data_dir / "accounts.sqlite") as conn:
        stored = conn.execute("SELECT token_hash FROM accounts").fetchone()[0]
    assert stored == sha256_hex(token.encode())


def test_taken_pseudonym_is_409_and_returns_no_token(client):
    _create(client, "mavi_kalem")
    response = _create(client, "MAVI_KALEM")
    assert_error(response, 409, "pseudonym_taken")
    assert "token" not in response.text


@pytest.mark.parametrize("bad", ["ab", "a" * 33, "ali veli", "çiçek", "a/b", "a#b", "", "   "])
def test_invalid_pseudonym_is_422(client, bad):
    assert_error(_create(client, bad), 422, "invalid_request")


def test_missing_pseudonym_is_422(client):
    assert_error(client.post("/api/accounts", json={}), 422, "invalid_request")


def test_account_is_in_the_graph_with_pseudonym_only(client):
    iri = _create(client, "mavi_kalem").json()["account"]
    import pyoxigraph

    quads = list(state.graph_store().quads_for_pattern(pyoxigraph.NamedNode(iri), None, None))
    predicates = {q.predicate.value for q in quads}
    assert predicates == {"http://www.w3.org/1999/02/22-rdf-syntax-ns#type", ALT_NAME}
    assert {q.object.value for q in quads} == {f"{NAMESPACE}StudentAccount", "mavi_kalem"}


def test_real_identity_fields_are_ignored_and_stored_nowhere(client, data_dir):
    # K-007: gövdeye isim, numara, e-posta eklense bile hiçbir yere yazılmaz.
    _create(client, "mavi_kalem", name="Ali Veli", studentNumber="20231234", email="ali@example.com")
    graph_text = str(list(state.graph_store().quads_for_pattern(None, None, None)))
    db_text = (data_dir / "accounts.sqlite").read_bytes()
    for secret in ("Ali Veli", "20231234", "ali@example.com"):
        assert secret not in graph_text
        assert secret.encode() not in db_text
    with sqlite3.connect(data_dir / "accounts.sqlite") as conn:
        columns = {row[1] for row in conn.execute("PRAGMA table_info(accounts)")}
    assert columns == {"pseudonym", "account_iri", "token_hash", "created_at"}


# --- X-NoteProof-Token denetimi --------------------------------------------------------------------------

@pytest.fixture
def protected_route():
    """require_account'u kullanan geçici bir uç nokta (yazma uç noktaları ARD-3 ve ARD-4'te gelecek)."""

    def whoami(account: Annotated[str, Depends(require_account)]) -> dict[str, str]:
        return {"account": account}

    route = APIRoute("/api/_test/whoami", whoami)
    app.router.routes.insert(0, route)
    yield
    app.router.routes.remove(route)


def test_valid_token_identifies_the_account(client, protected_route):
    body = _create(client, "mavi_kalem").json()
    response = client.get("/api/_test/whoami", headers={"X-NoteProof-Token": body["token"]})
    assert response.status_code == 200
    assert response.json() == {"account": body["account"]}


def test_missing_token_is_401(client, protected_route):
    assert_error(client.get("/api/_test/whoami"), 401, "unauthorized")


def test_wrong_token_is_401(client, protected_route):
    _create(client, "mavi_kalem")
    assert_error(client.get("/api/_test/whoami", headers={"X-NoteProof-Token": "yanlis"}), 401, "unauthorized")


def test_health_needs_no_token(client):
    assert client.get("/api/health").status_code == 200
