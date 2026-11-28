# NOTEPROOF-FILE
# module:   anchor
# owner:    burak           second: arda
# story:    S1, S2
# contract: 02#5.5 Store.enqueue
# depends:  core.config.data_dir
# status:   stable
"""Kuyruk ve batch kayıtları (SQLite).

Kayıt servisi (Arda'nın modülü) ile benim modülüm arasındaki SÖZLEŞME:
    store.enqueue(note_hash_hex)
Kayıt servisi notu kaydedip yazar onayladıktan sonra yalnızca bunu çağırır.
Gerisini (ağaç, işlem, proof) timestamp servisi halleder.

Tablolar:
    queue    -> her not hash'i için bir satır. batch_id boşsa hâlâ bekliyor.
    batches  -> her günlük çalışma için bir satır: kök, txid, blok bilgisi, durum.

Batch durumları (yarıda kalan işler tekrar çalışınca kaldığı yerden devam eder):
    built      -> ağaç kuruldu, notlar batch'e atandı, işlem henüz gönderilmedi
    broadcast  -> işlem ağa gönderildi, onay bekleniyor
    confirmed  -> işlem bir bloğa girdi; proof'lar hazır

Not: Proposal'da kalıcı veri Oxigraph'ta tutuluyor. Bu SQLite yalnızca
timestamp servisinin kendi iş kuyruğu; ileride Oxigraph'a aktarılabilir.
"""

from __future__ import annotations

import json
import re
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from core.config import data_dir

from .merkle import PathStep

DB_FILE_NAME = "noteproof.sqlite"  # data/ altındaki düzen: 02 bölüm 2

_HEX64 = re.compile(r"^[0-9a-f]{64}$")

SCHEMA = """
CREATE TABLE IF NOT EXISTS batches (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    day           TEXT NOT NULL,
    merkle_root   TEXT NOT NULL,
    status        TEXT NOT NULL CHECK (status IN ('built', 'broadcast', 'confirmed')),
    txids         TEXT NOT NULL DEFAULT '[]',  -- fee bump olursa birden fazla txid olur
    txid          TEXT,                         -- onaylanan (son) txid
    block_height  INTEGER,
    block_hash    TEXT,
    block_time    INTEGER
);
CREATE TABLE IF NOT EXISTS queue (
    note_hash      TEXT PRIMARY KEY,
    registered_at  TEXT NOT NULL,
    batch_id       INTEGER REFERENCES batches(id),
    leaf_index     INTEGER,
    merkle_path    TEXT
);
"""


@dataclass
class Batch:
    id: int
    day: str
    merkle_root: str
    status: str
    txids: list[str]
    txid: str | None
    block_height: int | None
    block_hash: str | None
    block_time: int | None


@dataclass
class QueuedNote:
    note_hash: str
    registered_at: str
    leaf_index: int | None
    merkle_path: list[PathStep] | None


def default_db_path() -> Path:
    """Kuyruğun varsayılan yeri: <veri klasörü>/noteproof.sqlite (NOTEPROOF_DATA_DIR, yoksa ./data)."""
    return data_dir() / DB_FILE_NAME


def path_to_json(path: list[PathStep]) -> str:
    return json.dumps([{"side": s.side, "sibling": s.sibling.hex()} for s in path])


def path_from_json(text: str) -> list[PathStep]:
    return [PathStep(s["side"], bytes.fromhex(s["sibling"])) for s in json.loads(text)]


class Store:
    def __init__(self, path: str | None = None):
        if path is None:
            path = str(default_db_path())
        if path != ":memory:":
            # data/ ilk çalıştırmada henüz yoktur; core.config klasörü oluşturmaz, yazan modül oluşturur.
            Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)

    def close(self) -> None:
        self.conn.close()

    # --- Kayıt servisinin kullandığı kısım -------------------------------------

    # NP-CONTRACT(02#5.5): imza sabit. Kayıt servisi (Arda) yalnızca bunu çağırır.
    def enqueue(self, note_hash_hex: str, registered_at: str | None = None) -> bool:
        """Bir not hash'ini bir sonraki günlük timestamp için kuyruğa ekler.

        Dönüş: True eklendi, False bu hash zaten kayıtlıydı (aynı dosya ikinci kez
        yüklenmiş; proposal adım 3'e göre önceki kaydı göstermek gerekir).
        """
        note_hash_hex = note_hash_hex.lower()
        if not _HEX64.match(note_hash_hex):
            raise ValueError("Not hash'i 64 karakterlik hex (SHA-256) olmalı")
        registered_at = registered_at or datetime.now(timezone.utc).isoformat(timespec="seconds")
        with self.conn:
            cursor = self.conn.execute(
                "INSERT OR IGNORE INTO queue (note_hash, registered_at) VALUES (?, ?)",
                (note_hash_hex, registered_at),
            )
        return cursor.rowcount == 1

    # --- Timestamp servisinin kullandığı kısım ---------------------------------

    def pending_hashes(self) -> list[str]:
        """Henüz bir batch'e girmemiş hash'ler, kayıt sırasına göre."""
        rows = self.conn.execute(
            "SELECT note_hash FROM queue WHERE batch_id IS NULL ORDER BY registered_at, rowid"
        )
        return [r["note_hash"] for r in rows]

    def create_batch(self, day: str, root: bytes, note_hashes: list[str], paths: list[list[PathStep]]) -> int:
        """Ağacı kaydeder ve notları batch'e atar (tek transaction'da, yarım kalmaz)."""
        with self.conn:
            cursor = self.conn.execute(
                "INSERT INTO batches (day, merkle_root, status) VALUES (?, ?, 'built')",
                (day, root.hex()),
            )
            batch_id = cursor.lastrowid
            for index, (note_hash, path) in enumerate(zip(note_hashes, paths, strict=True)):
                self.conn.execute(
                    "UPDATE queue SET batch_id = ?, leaf_index = ?, merkle_path = ? WHERE note_hash = ?",
                    (batch_id, index, path_to_json(path), note_hash),
                )
        return batch_id

    def add_txid(self, batch_id: int, txid: str) -> None:
        """Gönderilen (ya da fee bump ile yenilenen) işlemin txid'sini ekler."""
        batch = self.get_batch(batch_id)
        txids = batch.txids + [txid]
        with self.conn:
            self.conn.execute(
                "UPDATE batches SET status = 'broadcast', txids = ? WHERE id = ?",
                (json.dumps(txids), batch_id),
            )

    def mark_confirmed(self, batch_id: int, txid: str, block_height: int, block_hash: str, block_time: int) -> None:
        with self.conn:
            self.conn.execute(
                """UPDATE batches SET status = 'confirmed', txid = ?, block_height = ?,
                   block_hash = ?, block_time = ? WHERE id = ?""",
                (txid, block_height, block_hash, block_time, batch_id),
            )

    def unfinished_batches(self) -> list[Batch]:
        rows = self.conn.execute("SELECT * FROM batches WHERE status != 'confirmed' ORDER BY id")
        return [self._batch(r) for r in rows]

    def get_batch(self, batch_id: int) -> Batch:
        row = self.conn.execute("SELECT * FROM batches WHERE id = ?", (batch_id,)).fetchone()
        if row is None:
            raise KeyError(batch_id)
        return self._batch(row)

    def notes_in_batch(self, batch_id: int) -> list[QueuedNote]:
        rows = self.conn.execute(
            "SELECT * FROM queue WHERE batch_id = ? ORDER BY leaf_index", (batch_id,)
        )
        return [
            QueuedNote(
                note_hash=r["note_hash"],
                registered_at=r["registered_at"],
                leaf_index=r["leaf_index"],
                merkle_path=path_from_json(r["merkle_path"]) if r["merkle_path"] else None,
            )
            for r in rows
        ]

    @staticmethod
    def _batch(row: sqlite3.Row) -> Batch:
        return Batch(
            id=row["id"],
            day=row["day"],
            merkle_root=row["merkle_root"],
            status=row["status"],
            txids=json.loads(row["txids"]),
            txid=row["txid"],
            block_height=row["block_height"],
            block_hash=row["block_hash"],
            block_time=row["block_time"],
        )
