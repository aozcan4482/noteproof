# NOTEPROOF-FILE
# module:   core
# owner:    arda            second: burak
# story:    S1
# contract: 02#5.1
# depends:  core.hashing.sha256_hex
# status:   stable
"""core/hashing.py testleri: bilinen SHA-256 vektörleri ve tek karakter değişikliği."""

from __future__ import annotations

import re

import pytest

from core.hashing import sha256_hex


def test_known_vectors():
    # FIPS 180-2 örnekleri.
    assert sha256_hex(b"") == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    assert sha256_hex(b"abc") == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"


def test_result_is_lowercase_64_hex():
    assert re.fullmatch(r"[0-9a-f]{64}", sha256_hex(b"\x00\xff" * 1000))


def test_s1_one_changed_character_gives_a_different_hash():
    # 01 bölüm 7 reddetme senaryosunun temeli: tek karakteri değişen dosya aynı nota eşleşmez.
    assert sha256_hex(b"Transaction fees notu") != sha256_hex(b"Transaction fees nota")


def test_accepts_bytearray_and_memoryview():
    assert sha256_hex(bytearray(b"abc")) == sha256_hex(b"abc") == sha256_hex(memoryview(b"abc"))


def test_rejects_str():
    with pytest.raises(TypeError):
        sha256_hex("abc")
