# NOTEPROOF-FILE
# module:   register
# owner:    arda            second: burak
# story:    S1
# contract: 02#7 GET /api/health, hata biçimi
# depends:  register.app.app
# status:   wip
"""register/app.py testleri (ARD-1): sağlık kontrolü, ortak hata biçimi, web/ sayfalarının sunumu."""

from __future__ import annotations

import pytest

# FastAPI'nin test istemcisi httpx ister.
# NP-TODO(burak): httpx pyproject.toml dev grubuna girince bu satır importorskip'siz içe aktarmaya dönebilir.
pytest.importorskip("httpx")

from fastapi.routing import APIRoute  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from register.app import app  # noqa: E402

client = TestClient(app)


def _assert_error(response, status: int, code: str) -> None:
    assert response.status_code == status
    body = response.json()
    assert set(body) == {"error"}
    assert body["error"]["code"] == code
    assert isinstance(body["error"]["message"], str) and body["error"]["message"]


def test_s1_health_returns_ok():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.parametrize("method", ["GET", "POST", "DELETE"])
def test_unknown_api_path_is_404_in_common_format(method):
    _assert_error(client.request(method, "/api/yok"), 404, "not_found")


def test_nested_unknown_api_path_is_404():
    _assert_error(client.get("/api/notes/abc/yok"), 404, "not_found")


def test_wrong_method_on_known_path_is_405():
    response = client.post("/api/health")
    _assert_error(response, 405, "method_not_allowed")
    assert "GET" in response.headers["allow"]


def test_unknown_page_is_404_in_common_format():
    _assert_error(client.get("/yok.html"), 404, "not_found")


def test_web_pages_are_served_from_root():
    index = client.get("/")
    assert index.status_code == 200
    assert "text/html" in index.headers["content-type"]
    assert client.get("/proof.html").status_code == 200
    assert client.get("/js/config.js").status_code == 200


@pytest.fixture
def temporary_route():
    """Yalnızca bu test için, yakalayıcıdan ve statik sunumdan önce çalışan geçici uç noktalar."""

    def boom() -> None:
        raise RuntimeError("iç ayrıntı: data/notes/gizli.pdf")

    def needs_int(n: int) -> dict[str, int]:
        return {"n": n}

    added = [APIRoute("/api/_test/boom", boom), APIRoute("/api/_test/int", needs_int)]
    for route in reversed(added):
        app.router.routes.insert(0, route)
    yield
    for route in added:
        app.router.routes.remove(route)


def test_unexpected_error_is_500_without_details(temporary_route):
    response = TestClient(app, raise_server_exceptions=False).get("/api/_test/boom")
    _assert_error(response, 500, "internal_error")
    assert "gizli" not in response.text


def test_invalid_parameter_is_422_invalid_request(temporary_route):
    _assert_error(client.get("/api/_test/int?n=sayi-degil"), 422, "invalid_request")


def test_error_body_omits_empty_violations():
    from register.errors import error_body

    assert error_body("not_found", "x") == {"error": {"code": "not_found", "message": "x"}}
    v = [{"shape": "NoteShape", "path": "np:topic", "message": "m"}]
    assert error_body("shape_violation", "x", v)["error"]["violations"] == v
