# NOTEPROOF-FILE
# module:   tagger
# owner:    aleyna          second: eylem
# story:    S3
# contract: 02#5.3, 02#8
# depends:  tagger.llm.client_from_env, tagger.llm.GroqClient
# status:   stable
"""tagger/llm.py testleri: arayüz, Groq istemcisi ve ortam değişkenlerinden kurulum.

Ağa çıkılmaz: GroqClient'a sahte bir urlopen verilir, beklemeler de sahte sleep ile kaydedilir.
"""

from __future__ import annotations

import email.message
import io
import json
import urllib.error

import pytest

from tagger.llm import ENV_API_KEY, ENV_MODEL, ENV_PROVIDER, GroqClient, LLMClient, client_from_env

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


KEY = "gsk_test_gizli_anahtar"


class FakeUrlopen:
    """urllib.request.urlopen yerine geçer: sırayla verilen yanıtları ya da hataları döndürür."""

    def __init__(self, *outcomes):
        self._outcomes = list(outcomes)
        self.requests = []

    def __call__(self, request, *, timeout, context):
        self.requests.append(request)
        outcome = self._outcomes.pop(0)
        if isinstance(outcome, Exception):
            raise outcome
        return io.BytesIO(json.dumps(outcome).encode())


def ok(content):
    return {"choices": [{"message": {"role": "assistant", "content": content}}]}


def http_error(status, retry_after=None):
    headers = email.message.Message()
    if retry_after is not None:
        headers["Retry-After"] = retry_after
    return urllib.error.HTTPError("https://api.groq.com", status, "hata", headers, None)


def groq(fake, sleeps=None):
    return GroqClient("openai/gpt-oss-20b", KEY, urlopen=fake, sleep=(sleeps if sleeps is not None else []).append)


def test_groq_client_satisfies_the_llmclient_interface():
    assert isinstance(groq(FakeUrlopen()), LLMClient)


def test_groq_client_sends_model_messages_and_key_and_returns_the_text():
    fake = FakeUrlopen(ok('{"course": "Course_SEN0401"}'))
    answer = groq(fake).complete("not metni", system="sistem")

    assert answer == '{"course": "Course_SEN0401"}'
    request = fake.requests[0]
    body = json.loads(request.data)
    assert request.full_url == "https://api.groq.com/openai/v1/chat/completions"
    assert request.get_method() == "POST"
    assert request.get_header("Authorization") == f"Bearer {KEY}"
    assert body["model"] == "openai/gpt-oss-20b"
    assert body["messages"] == [{"role": "system", "content": "sistem"}, {"role": "user", "content": "not metni"}]


def test_groq_client_without_system_sends_only_the_user_message():
    fake = FakeUrlopen(ok("{}"))
    groq(fake).complete("not metni")
    assert json.loads(fake.requests[0].data)["messages"] == [{"role": "user", "content": "not metni"}]


def test_groq_client_empty_content_is_an_empty_string_not_an_error():
    assert groq(FakeUrlopen(ok(None))).complete("not") == ""


def test_groq_client_retries_after_429_and_honours_retry_after():
    sleeps = []
    fake = FakeUrlopen(http_error(429, retry_after="7"), http_error(503), ok("{}"))
    assert groq(fake, sleeps).complete("not") == "{}"
    assert len(fake.requests) == 3
    assert sleeps == [7.0, 2.0]  # Retry-After'a uyuldu, sonra 2**1 sn


def test_groq_client_gives_up_after_max_retries_with_a_clear_error():
    sleeps = []
    fake = FakeUrlopen(*[http_error(429)] * 4)
    with pytest.raises(RuntimeError) as err:
        groq(fake, sleeps).complete("not")
    assert "429" in str(err.value)
    assert len(fake.requests) == 4 and sleeps == [1.0, 2.0, 4.0]


def test_groq_client_does_not_retry_a_wrong_key_and_never_prints_it():
    fake = FakeUrlopen(http_error(401))
    with pytest.raises(RuntimeError) as err:
        groq(fake).complete("gizli not metni")
    assert len(fake.requests) == 1
    assert "401" in str(err.value)
    assert KEY not in str(err.value) and "gizli not metni" not in str(err.value)
    assert KEY not in repr(groq(FakeUrlopen()))


def test_groq_client_network_failure_is_retried_then_reported():
    sleeps = []
    fake = FakeUrlopen(*[urllib.error.URLError("bağlantı yok")] * 4)
    with pytest.raises(RuntimeError) as err:
        groq(fake, sleeps).complete("not")
    assert "bağlanılamadı" in str(err.value) and len(sleeps) == 3


def test_groq_client_unexpected_response_shape_is_a_clear_error():
    with pytest.raises(RuntimeError):
        groq(FakeUrlopen({"error": "?"})).complete("not")


def test_client_from_env_builds_a_groq_client(monkeypatch):
    monkeypatch.setenv(ENV_PROVIDER, " Groq ")
    monkeypatch.setenv(ENV_MODEL, "openai/gpt-oss-20b")
    monkeypatch.setenv(ENV_API_KEY, KEY)
    client = client_from_env()
    assert isinstance(client, GroqClient) and client.model == "openai/gpt-oss-20b"
