# NOTEPROOF-FILE
# module:   anchor
# owner:    burak           second: arda
# story:    S1, S2, S7
# contract: -
# depends:  -
# status:   stable
"""daily.py akış testleri — sahte node ile (bitcoind gerekmez)."""

import hashlib
import json

import pytest

from anchor import daily, opreturn, proof
from anchor.store import Store

from .fake_rpc import FakeRPC


def notes(n):
    files = [f"Ders notu {i}: Transaction fees".encode() for i in range(n)]
    return files, [hashlib.sha256(f).hexdigest() for f in files]


@pytest.fixture
def store(tmp_path):
    s = Store(str(tmp_path / "q.sqlite"))
    yield s
    s.close()


def run(store, rpc, out, **kw):
    return daily.run_daily(store, rpc, out, day="2026-11-12", sleep=lambda _: None, before_poll=rpc.mine, **kw)


def test_40_notes_one_transaction_and_valid_proofs(store, tmp_path):
    files, hashes = notes(40)
    for h in hashes:
        assert store.enqueue(h)
    rpc = FakeRPC()
    out = tmp_path / "proofs"

    (batch,) = run(store, rpc, out)

    # 40 not -> tek işlem (story 2)
    assert rpc.calls.count("sendrawtransaction") == 1
    assert batch.status == "confirmed"
    for f, h in zip(files, hashes):
        p = json.loads((out / f"{h}.json").read_text())
        assert proof.verify_offline(p, f)[0]
        assert proof.verify_on_chain(p, rpc)[0]
    # Kuyruk boşaldı; tekrar çalışınca yeni işlem gönderilmez.
    assert run(store, rpc, out) == []
    assert rpc.calls.count("sendrawtransaction") == 1


def test_changed_file_is_not_the_registered_file(store, tmp_path):
    files, hashes = notes(3)
    for h in hashes:
        store.enqueue(h)
    rpc = FakeRPC()
    run(store, rpc, tmp_path)
    p = json.loads((tmp_path / f"{hashes[0]}.json").read_text())
    tampered = files[0][:-1] + b"X"   # tek karakter değişti (proposal senaryosu)
    ok, message = proof.verify_offline(p, tampered)
    assert not ok and "kayıtlı dosya değil" in message


def test_only_32_byte_roots_reach_the_chain(store, tmp_path):
    _, hashes = notes(5)
    for h in hashes:
        store.enqueue(h)
    rpc = FakeRPC()
    run(store, rpc, tmp_path)
    for txid in rpc.sent:
        decoded = rpc.call("decoderawtransaction", rpc.txs[txid]["hex"])
        assert opreturn.tx_holds_only_root(decoded)


def test_empty_queue_does_nothing(store, tmp_path):
    rpc = FakeRPC()
    assert run(store, rpc, tmp_path) == []
    assert "sendrawtransaction" not in rpc.calls


def test_duplicate_hash_is_not_queued_twice(store):
    _, (h,) = notes(1)
    assert store.enqueue(h) is True
    assert store.enqueue(h) is False
    assert store.pending_hashes() == [h]


def test_refuses_mainnet(store, tmp_path):
    _, hashes = notes(1)
    store.enqueue(hashes[0])
    with pytest.raises(RuntimeError):
        run(store, FakeRPC(chain="main"), tmp_path)


def test_fee_bump_after_6_blocks(store, tmp_path):
    files, hashes = notes(4)
    for h in hashes:
        store.enqueue(h)
    rpc = FakeRPC(stuck_first=True)
    (batch,) = run(store, rpc, tmp_path, max_blocks=6)
    assert "bumpfee" in rpc.calls
    assert len(batch.txids) == 2 and batch.txid == batch.txids[1]
    p = json.loads((tmp_path / f"{hashes[2]}.json").read_text())
    assert proof.verify_on_chain(p, rpc)[0]


def test_resumes_batch_left_unfinished(store, tmp_path):
    # Önceki çalışma ağacı kurup işlem göndermeden çökmüş gibi davran.
    _, hashes = notes(3)
    for h in hashes:
        store.enqueue(h)
    from anchor import merkle
    root, paths = merkle.build_tree([bytes.fromhex(h) for h in hashes])
    store.create_batch("2026-11-11", root, hashes, paths)
    assert store.pending_hashes() == []

    rpc = FakeRPC()
    (batch,) = run(store, rpc, tmp_path)
    assert batch.day == "2026-11-11" and batch.status == "confirmed"
    assert rpc.calls.count("sendrawtransaction") == 1
