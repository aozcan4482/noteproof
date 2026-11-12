"""Gerçek bitcoind ile regtest testi (proposal test case: 40 not, tek işlem).

bitcoind kurulu değilse otomatik atlanır. Kurmak için (macOS): brew install bitcoin
CI'da (GitHub Actions) bitcoind kurulup bu test her push'ta çalışacak.
"""

import hashlib
import json
import shutil
import socket
import subprocess
import time

import pytest

from anchor import daily, opreturn, proof
from anchor.rpc import BitcoinRPC, RpcError
from anchor.store import Store

pytestmark = [
    pytest.mark.regtest,
    pytest.mark.skipif(shutil.which("bitcoind") is None, reason="bitcoind kurulu değil"),
]


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture(scope="module")
def node(tmp_path_factory):
    datadir = tmp_path_factory.mktemp("bitcoin")
    port = free_port()
    proc = subprocess.Popen(
        [
            "bitcoind", "-regtest", f"-datadir={datadir}", f"-rpcport={port}",
            f"-port={free_port()}", "-rpcuser=test", "-rpcpassword=test",
            "-fallbackfee=0.0002", "-listen=0", "-printtoconsole=0",
        ]
    )
    base = BitcoinRPC(f"http://127.0.0.1:{port}", "test", "test")
    for _ in range(100):  # node açılana kadar bekle
        try:
            base.call("getblockcount")
            break
        except (OSError, RpcError):
            time.sleep(0.2)
    else:
        proc.kill()
        pytest.fail("bitcoind açılmadı")
    base.call("createwallet", "noteproof")
    rpc = BitcoinRPC(f"http://127.0.0.1:{port}", "test", "test", wallet="noteproof")
    address = rpc.call("getnewaddress")
    rpc.call("generatetoaddress", 101, address)  # coinbase'ler harcanabilir olsun
    rpc.address = address
    yield rpc
    base.call("stop")
    proc.wait(timeout=30)


def test_40_notes_anchored_on_regtest(node, tmp_path):
    files = [f"Regtest notu {i}".encode() for i in range(40)]
    hashes = [hashlib.sha256(f).hexdigest() for f in files]
    store = Store(str(tmp_path / "q.sqlite"))
    for h in hashes:
        store.enqueue(h)

    (batch,) = daily.run_daily(
        store, node, tmp_path / "proofs", day="2026-11-12",
        sleep=lambda _: None,
        before_poll=lambda: node.call("generatetoaddress", 1, node.address),
    )

    # Tek işlem, içinde yalnızca 32 byte'lık kök (DoD).
    tx = node.call("getrawtransaction", batch.txid, True, batch.block_hash)
    assert opreturn.tx_holds_only_root(tx)
    assert opreturn.parse_root(opreturn.op_return_outputs(tx)[0]).hex() == batch.merkle_root

    for f, h in zip(files, hashes):
        p = json.loads((tmp_path / "proofs" / f"{h}.json").read_text())
        assert p["network"] == "regtest"
        assert proof.verify_offline(p, f)[0]
        assert proof.verify_on_chain(p, node)[0]
    store.close()
