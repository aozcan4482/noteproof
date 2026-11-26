# NOTEPROOF-FILE
# module:   tagger
# owner:    aleyna          second: eylem
# story:    S3
# contract: 02#5.3, 02#8
# depends:  tagger.llm.client_from_env
# status:   wip
"""tagger/llm.py testleri: arayüz ve ortam değişkenlerinden istemci kurulumu. Ağa çıkılmaz."""

from __future__ import annotations

import pytest

from tagger.llm import ENV_API_KEY, ENV_MODEL, ENV_PROVIDER, LLMClient, client_from_env

from .fake_llm import FakeLLM


def test_fake_llm_satisfies_the_llmclient_interface():
    assert isinstance(FakeLLM("{}"), LLMClient)


def test_client_from_env_without_settings_raises_a_clear_error(monkeypatch):
    for name in (ENV_PROVIDER, ENV_MODEL, ENV_API_KEY):
        monkeypatch.delenv(name, raising=False)
    with pytest.raises(RuntimeError) as err:
        client_from_env()
    assert ENV_API_KEY in str(err.value)


def test_client_from_env_never_prints_the_api_key(monkeypatch):
    monkeypatch.setenv(ENV_PROVIDER, "bilinmeyen")
    monkeypatch.setenv(ENV_MODEL, "model")
    monkeypatch.setenv(ENV_API_KEY, "gizli-anahtar-123")
    with pytest.raises(RuntimeError) as err:
        client_from_env()
    assert "gizli-anahtar-123" not in str(err.value)
