# NOTEPROOF-FILE
# module:   anchor
# owner:    burak           second: arda
# story:    S1, S2
# contract: 02#5.5 günlük iş, mainnet reddi
# depends:  core.config.data_dir
# status:   stable
"""Günlük timestamp işi — proposal aktivite modeli B (adım 10-13).

Her gün 23:00'te (cron ile) çalışır:
    10. Kuyruktaki, henüz zincire yazılmamış hash'leri topla. Boşsa bitir.
    11. Merkle tree'yi kur; 32 byte'lık kökü OP_RETURN çıktısına koy.
    12. İşlemi Bitcoin Core üzerinden signet'e gönder, 1 onay bekle.
        6 blok içinde onaylanmazsa fee'yi artır (bumpfee) ve tekrar bekle.
    13. txid'yi, blok yüksekliğini ve her notun path'ini kaydet, proof dosyalarını yaz.

Çalıştırma:
    export NOTEPROOF_RPC_USER=... NOTEPROOF_RPC_PASSWORD=... NOTEPROOF_RPC_WALLET=noteproof
    python -m anchor.daily
    (varsayılanlar: data/noteproof.sqlite ve data/proofs/; NOTEPROOF_DATA_DIR ile değişir,
     elle vermek için: --db data/noteproof.sqlite --out data/proofs)

Güvenlik: mainnet'te çalışmayı reddeder (proposal kapsam dışı: "Bitcoin mainnet").
"""

from __future__ import annotations

import argparse
import json
import time
from datetime import date
from pathlib import Path
from typing import Callable

from core.config import data_dir

from . import merkle, opreturn
from .proof import build_proof
from .rpc import BitcoinRPC, RpcError
from .store import Batch, Store, default_db_path

PROOFS_DIR_NAME = "proofs"  # data/proofs/<hash>.json (02 bölüm 2)

# NP-CONTRACT(02#5.5): mainnet reddedilir; bu kontrol kaldırılmaz (03 bölüm 9).
ALLOWED_CHAINS = {"signet", "regtest", "test", "testnet4"}


def check_network(rpc) -> str:
    chain = rpc.call("getblockchaininfo")["chain"]
    if chain not in ALLOWED_CHAINS:
        raise RuntimeError(f"'{chain}' ağında çalışılmaz; yalnızca signet/regtest kullanılır")
    return chain


def broadcast_root(rpc, root: bytes) -> str:
    """Kökü taşıyan işlemi oluşturur, cüzdandan fonlar, imzalar ve gönderir. txid döner.

    createrawtransaction'daki {"data": ...} çıktısı Bitcoin Core'da OP_RETURN demektir.
    Girdi vermiyoruz; fundrawtransaction cüzdandan uygun UTXO'yu ve para üstünü ekler.
    replaceable=True: işlem RBF'li olur, böylece gerekirse bumpfee ile fee artırılabilir.
    """
    opreturn.build_script(root)  # 32 byte değilse burada hata verir; zincire başka şey gitmez
    raw = rpc.call("createrawtransaction", [], [{"data": root.hex()}])
    funded = rpc.call("fundrawtransaction", raw, {"replaceable": True})
    signed = rpc.call("signrawtransactionwithwallet", funded["hex"])
    if not signed.get("complete"):
        raise RuntimeError("İşlem imzalanamadı")
    decoded = rpc.call("decoderawtransaction", signed["hex"])
    if not opreturn.tx_holds_only_root(decoded):
        raise RuntimeError("İşlemde 32 byte'lık kök dışında OP_RETURN verisi var; gönderilmedi")
    return rpc.call("sendrawtransaction", signed["hex"])


def wait_for_confirmation(
    rpc,
    txids: list[str],
    on_new_txid: Callable[[str], None],
    *,
    max_blocks: int = 6,
    poll_seconds: float = 30,
    sleep: Callable[[float], None] = time.sleep,
    before_poll: Callable[[], None] | None = None,
) -> tuple[str, dict]:
    """İşlemlerden biri 1 onay alana kadar bekler. (onaylanan txid, gettransaction sonucu) döner.

    Fee bump sonrası eski ve yeni işlem birbirinin yerine geçer; hangisi bloğa
    girerse o geçerlidir, bu yüzden hepsini kontrol ediyoruz.
    before_poll: testlerde regtest'te blok üretmek için kullanılır.
    """
    txids = list(txids)
    start_height = rpc.call("getblockcount")
    while True:
        if before_poll:
            before_poll()
        for txid in txids:
            tx = rpc.call("gettransaction", txid)
            if tx.get("confirmations", 0) >= 1:
                return txid, tx
        height = rpc.call("getblockcount")
        if height - start_height >= max_blocks:
            new_txid = rpc.call("bumpfee", txids[-1])["txid"]
            txids.append(new_txid)
            on_new_txid(new_txid)
            start_height = height
        sleep(poll_seconds)


def write_proofs(store: Store, batch: Batch, network: str, out_dir: Path) -> list[Path]:
    """Onaylanmış batch'teki her not için <noteHash>.json proof dosyası yazar."""
    out_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for note in store.notes_in_batch(batch.id):
        proof = build_proof(
            note.note_hash, note.merkle_path, batch.merkle_root, batch.txid,
            batch.block_height, batch.block_hash, batch.block_time, network,
        )
        path = out_dir / f"{note.note_hash}.json"
        path.write_text(json.dumps(proof, indent=2))
        written.append(path)
    return written


def finish_batch(store: Store, rpc, batch: Batch, network: str, out_dir: Path, **wait_kwargs) -> Batch:
    """Bir batch'i (yeni ya da yarıda kalmış) onaylanana kadar götürür ve proof'ları yazar."""
    if batch.status == "built":
        txid = broadcast_root(rpc, bytes.fromhex(batch.merkle_root))
        store.add_txid(batch.id, txid)
        batch = store.get_batch(batch.id)
    txid, tx = wait_for_confirmation(
        rpc, batch.txids, lambda t: store.add_txid(batch.id, t), **wait_kwargs
    )
    store.mark_confirmed(batch.id, txid, tx["blockheight"], tx["blockhash"], tx["blocktime"])
    batch = store.get_batch(batch.id)
    write_proofs(store, batch, network, out_dir)
    return batch


def run_daily(store: Store, rpc, out_dir: Path, day: str | None = None, **wait_kwargs) -> list[Batch]:
    """Günlük işin tamamı. Tamamlanan batch'leri döndürür (hiç iş yoksa boş liste)."""
    network = check_network(rpc)
    done = []
    # Önce önceki çalışmalardan yarıda kalan batch var mı? (örn. sunucu çöktüyse)
    for batch in store.unfinished_batches():
        done.append(finish_batch(store, rpc, batch, network, out_dir, **wait_kwargs))

    pending = store.pending_hashes()          # adım 10
    if not pending:
        return done
    root, paths = merkle.build_tree([bytes.fromhex(h) for h in pending])   # adım 11
    batch_id = store.create_batch(day or date.today().isoformat(), root, pending, paths)
    done.append(finish_batch(store, rpc, store.get_batch(batch_id), network, out_dir, **wait_kwargs))  # 12-13
    return done


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="NoteProof günlük Bitcoin timestamp işi")
    parser.add_argument("--db", default=str(default_db_path()), help="kuyruk veritabanı (varsayılan: %(default)s)")
    parser.add_argument(
        "--out", default=str(data_dir() / PROOFS_DIR_NAME),
        help="proof dosyalarının yazılacağı klasör (varsayılan: %(default)s)",
    )
    parser.add_argument("--max-blocks", type=int, default=6, help="bu kadar blokta onay yoksa fee artır")
    parser.add_argument("--poll", type=float, default=30, help="onay kontrolleri arası saniye")
    args = parser.parse_args(argv)

    store = Store(args.db)
    try:
        batches = run_daily(
            store, BitcoinRPC.from_env(), Path(args.out),
            max_blocks=args.max_blocks, poll_seconds=args.poll,
        )
    except RpcError as e:
        print(f"Bitcoin node hatası: {e}")
        return 1
    finally:
        store.close()
    if not batches:
        print("Kuyruk boş, bugün zincire yazılacak not yok.")
    for b in batches:
        print(f"Batch {b.id}: kök {b.merkle_root} -> txid {b.txid} (blok {b.block_height})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
