# NOTEPROOF-FILE
# module:   anchor
# owner:    burak           second: arda
# story:    S1
# contract: 02#2 çalışma verisi data/ altında, 02#3 namespace tek yerde
# depends:  core.config.data_dir, core.ns
# status:   stable
"""Varsayılan yollar data/ altında mı, namespace core.ns'ten mi geliyor? (BRK-4)"""

from __future__ import annotations

from pathlib import Path

from anchor import daily, proof, store
from core import ns

HASH = "a" * 64


def test_s1_default_queue_lives_under_data_dir(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("NOTEPROOF_DATA_DIR", raising=False)
    s = store.Store()  # data/ henüz yok: Store kendisi oluşturur
    assert s.enqueue(HASH)
    s.close()
    assert (tmp_path / "data" / "noteproof.sqlite").is_file()
    assert not (tmp_path / "noteproof.sqlite").exists()


def test_s1_data_dir_variable_moves_the_queue(tmp_path, monkeypatch):
    monkeypatch.setenv("NOTEPROOF_DATA_DIR", str(tmp_path / "veri"))
    assert store.default_db_path() == tmp_path / "veri" / "noteproof.sqlite"


def test_s1_daily_job_defaults_point_under_data_dir(tmp_path, monkeypatch):
    # main() argümansız çalışınca kuyruğu ve proof klasörünü veri klasöründen almalı.
    monkeypatch.setenv("NOTEPROOF_DATA_DIR", str(tmp_path))
    seen = {}

    def fake_run_daily(queue, rpc, out_dir, **kwargs):
        seen["out"] = Path(out_dir)
        return []

    monkeypatch.setattr(daily, "run_daily", fake_run_daily)
    monkeypatch.setattr(daily.BitcoinRPC, "from_env", classmethod(lambda cls: None))
    assert daily.main([]) == 0
    assert seen["out"] == tmp_path / "proofs"
    assert (tmp_path / "noteproof.sqlite").is_file()


def test_s1_proof_namespace_comes_from_core():
    assert proof.NAMESPACE is ns.NAMESPACE
    assert f"{proof.NAMESPACE}proof/{HASH}" == ns.proof_iri(HASH)
