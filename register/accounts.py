# NOTEPROOF-FILE
# module:   register
# owner:    arda            second: burak
# story:    S1
# contract: 02#7 POST /api/accounts, X-NoteProof-Token; K-007
# depends:  core.ns.account_iri, core.hashing.sha256_hex
# status:   wip
"""Takma adlı hesaplar ve token denetimi (K-007).

Öğrenci bir takma ad seçer; sistem rastgele bir token üretir ve onu yalnızca bir kez gösterir. Token'ın
kendisi hiçbir yerde saklanmaz, yalnızca SHA-256 özeti saklanır. Gerçek isim, öğrenci numarası ve e-posta
istenmez ve saklanmaz.

Saklama iki yerdedir:
- Grafik (Oxigraph): hesap IRI'si np:StudentAccount ve schema:alternateName (02 bölüm 4). Notlar bu IRI'ye
  prov:wasAttributedTo ile bağlanır; arama servisi (Erdener) yazarın takma adını buradan okur.
- data/accounts.sqlite: hesap IRI'si ve token özeti. Yalnızca kayıt servisi kullanır. Sır grafiğe girmez,
  böylece SPARQL sorgusuyla hiçbir yerden okunamaz.
"""

from __future__ import annotations

import pathlib
import re
import secrets
import sqlite3
from contextlib import closing
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from core.hashing import sha256_hex
from core.ns import NAMESPACE, account_iri

if TYPE_CHECKING:
    import pyoxigraph

# NP-TODO(erdener): 02 bölüm 2'deki data/ listesine "data/accounts.sqlite  hesaplar ve token özetleri" satırı.
ACCOUNTS_DB = "accounts.sqlite"

# Takma ad kuralı (Arda kararı, ARD-2): küçük harfe çevrilir; 3–32 karakter, yalnızca a-z, 0-9, _ ve -.
# Türkçe karakter ve boşluk yok: IRI temiz kalır ve "Ali" ile "ali" iki ayrı hesap olmaz.
PSEUDONYM_RE = re.compile(r"[a-z0-9_-]{3,32}")

# Token 32 rastgele byte'tır (secrets). Tahmin edilemeyecek kadar uzun olduğu için yavaş bir parola özeti
# (bcrypt gibi) gerekmez; tek SHA-256 yeterlidir ve standart kütüphane dışında bağımlılık getirmez.
TOKEN_BYTES = 32

RDF_TYPE = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
SCHEMA_ALTERNATE_NAME = "https://schema.org/alternateName"
NP_STUDENT_ACCOUNT = f"{NAMESPACE}StudentAccount"


class InvalidPseudonym(ValueError):
    """Takma ad kurala uymuyor."""


class PseudonymTaken(ValueError):
    """Bu takma adla bir hesap zaten var."""


def normalize_pseudonym(raw: str) -> str:
    """Takma adı küçük harfe çevirip kurala göre denetler; geçersizse InvalidPseudonym."""
    if not isinstance(raw, str):
        raise InvalidPseudonym("Takma ad metin olmalı.")
    pseudonym = raw.strip().lower()
    if not PSEUDONYM_RE.fullmatch(pseudonym):
        raise InvalidPseudonym("Takma ad 3–32 karakter olmalı; yalnızca a-z, 0-9, _ ve - kullanılabilir.")
    return pseudonym


def _token_hash(token: str) -> str:
    return sha256_hex(token.encode("utf-8"))


class AccountStore:
    """Hesap IRI'si ile token özetini tutan küçük SQLite tablosu.

    Her işlem kendi bağlantısını açar: FastAPI eşzamanlı uç noktaları farklı iş parçacıklarında çalıştırır
    ve sqlite3 bağlantısı iş parçacıkları arasında paylaşılmamalıdır.
    """

    def __init__(self, path: pathlib.Path) -> None:
        self.path = pathlib.Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with closing(self._connect()) as conn, conn:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS accounts ("
                " pseudonym TEXT PRIMARY KEY,"
                " account_iri TEXT NOT NULL UNIQUE,"
                " token_hash TEXT NOT NULL UNIQUE,"
                " created_at TEXT NOT NULL)"
            )

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.path)

    def create(self, pseudonym: str, graph: "pyoxigraph.Store") -> tuple[str, str]:
        """Hesabı açar; (hesap IRI'si, token) döner. Token'ı çağıran yalnızca bir kez gösterir.

        SQLite kaydı ve grafik üçlüleri birlikte yazılır: grafiğe yazma başarısız olursa SQLite işlemi geri
        alınır, böylece yarım hesap kalmaz.
        """
        import pyoxigraph

        pseudonym = normalize_pseudonym(pseudonym)
        iri = account_iri(pseudonym)
        token = secrets.token_urlsafe(TOKEN_BYTES)
        now = datetime.now(timezone.utc).isoformat(timespec="seconds")

        with closing(self._connect()) as conn:
            try:
                with conn:  # hata olursa geri alınır
                    conn.execute(
                        "INSERT INTO accounts (pseudonym, account_iri, token_hash, created_at) VALUES (?, ?, ?, ?)",
                        (pseudonym, iri, _token_hash(token), now),
                    )
                    subject = pyoxigraph.NamedNode(iri)
                    rdf_type = pyoxigraph.NamedNode(RDF_TYPE)
                    alt_name = pyoxigraph.NamedNode(SCHEMA_ALTERNATE_NAME)
                    graph.extend([
                        pyoxigraph.Quad(subject, rdf_type, pyoxigraph.NamedNode(NP_STUDENT_ACCOUNT)),
                        pyoxigraph.Quad(subject, alt_name, pyoxigraph.Literal(pseudonym)),
                    ])
            except sqlite3.IntegrityError as exc:
                raise PseudonymTaken(pseudonym) from exc
        return iri, token

    def account_for_token(self, token: str | None) -> str | None:
        """Token geçerliyse hesap IRI'sini, değilse None döndürür."""
        if not token:
            return None
        with closing(self._connect()) as conn:
            row = conn.execute(
                "SELECT account_iri FROM accounts WHERE token_hash = ?", (_token_hash(token),)
            ).fetchone()
        return row[0] if row else None
