# NOTEPROOF-FILE
# module:   register
# owner:    arda            second: burak
# story:    -
# contract: -
# depends:  register.app.app
# status:   wip
"""Kayıt servisi testlerinin ortak parçaları: her test kendi geçici veri klasörüyle çalışır."""

from __future__ import annotations

import gc

import pytest
from fastapi.testclient import TestClient

from register import state
from register.app import app


@pytest.fixture
def data_dir(monkeypatch, tmp_path):
    """NOTEPROOF_DATA_DIR'i geçici klasöre çevirir; grafik ve hesap tablosu her testte sıfırdan açılır."""
    monkeypatch.setenv("NOTEPROOF_DATA_DIR", str(tmp_path))
    state.reset()
    yield tmp_path
    state.reset()
    gc.collect()  # Oxigraph kilidi nesne bırakılınca kalkar


@pytest.fixture
def client(data_dir):
    return TestClient(app)


def assert_error(response, status: int, code: str) -> None:
    """Yanıt 02 bölüm 7'deki ortak hata biçiminde mi?"""
    assert response.status_code == status, response.text
    body = response.json()
    assert set(body) == {"error"}
    assert body["error"]["code"] == code
    assert isinstance(body["error"]["message"], str) and body["error"]["message"]
