# NOTEPROOF-FILE
# module:   anchor
# owner:    burak           second: arda
# story:    S2
# contract: 02#8 NOTEPROOF_RPC_*
# depends:  -
# status:   stable
"""Bitcoin Core JSON-RPC istemcisi.

Bitcoin Core node'u (bitcoind) bir HTTP sunucusu açar; ona JSON ile komut
göndeririz (bitcoin-cli'nin yaptığı şeyin aynısı). Ek kütüphane kullanmadan,
yalnızca urllib ile yazıldı.

Bağlantı ayarları ortam değişkenlerinden okunur (şifreler koda yazılmaz):
    NOTEPROOF_RPC_URL       örn. http://127.0.0.1:38332   (signet varsayılan portu)
    NOTEPROOF_RPC_USER
    NOTEPROOF_RPC_PASSWORD
    NOTEPROOF_RPC_WALLET    örn. noteproof  (fon tutan cüzdanın adı)
"""

from __future__ import annotations

import base64
import json
import os
import urllib.error
import urllib.request
from typing import Any


class RpcError(Exception):
    """Node'un döndürdüğü hata (örn. yetersiz bakiye, bilinmeyen txid)."""

    def __init__(self, code: int, message: str):
        super().__init__(f"RPC hata {code}: {message}")
        self.code = code
        self.message = message


class BitcoinRPC:
    def __init__(
        self,
        url: str,
        user: str,
        password: str,
        wallet: str | None = None,
        timeout: float = 30,
    ):
        self.base_url = url.rstrip("/")
        self.wallet = wallet
        self.timeout = timeout
        token = base64.b64encode(f"{user}:{password}".encode()).decode()
        self._auth_header = f"Basic {token}"

    @classmethod
    def from_env(cls) -> "BitcoinRPC":
        return cls(
            url=os.environ.get("NOTEPROOF_RPC_URL", "http://127.0.0.1:38332"),
            user=os.environ["NOTEPROOF_RPC_USER"],
            password=os.environ["NOTEPROOF_RPC_PASSWORD"],
            wallet=os.environ.get("NOTEPROOF_RPC_WALLET"),
        )

    @property
    def url(self) -> str:
        # Cüzdan komutları /wallet/<ad> adresine gider. Zincir komutları da bu
        # adreste çalıştığı için hepsini aynı yere gönderiyoruz.
        if self.wallet:
            return f"{self.base_url}/wallet/{self.wallet}"
        return self.base_url

    def call(self, method: str, *params: Any) -> Any:
        payload = json.dumps(
            {"jsonrpc": "1.0", "id": "noteproof", "method": method, "params": list(params)}
        ).encode()
        request = urllib.request.Request(
            self.url,
            data=payload,
            headers={"Content-Type": "application/json", "Authorization": self._auth_header},
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                body = json.loads(response.read())
        except urllib.error.HTTPError as e:
            # Bitcoin Core hatalarda HTTP 500 döner ama gövdede JSON hata vardır.
            try:
                body = json.loads(e.read())
            except (ValueError, OSError):
                raise RpcError(e.code, e.reason) from e
        if body.get("error"):
            raise RpcError(body["error"]["code"], body["error"]["message"])
        return body["result"]
