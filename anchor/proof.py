# NOTEPROOF-FILE
# module:   anchor
# owner:    burak           second: arda
# story:    S1, S7
# contract: 02#5.5, 02#6 proof dosyası
# depends:  core.ns.NAMESPACE
# status:   stable
"""Proof dosyası: bir notun zincirdeki kanıtı (JSON-LD).

Proposal'daki "Interface" bölümüne göre proof küçük bir JSON-LD dosyasıdır ve
proof sayfası YALNIZCA şunlarla çalışır:
    1) bu proof dosyası, 2) notun kendisi, 3) herhangi bir public signet node'u.
Arşivin sunucusu kapalı olsa bile kanıt kontrol edilebilir.

Doğrulama iki adımdır:
    verify_offline   -> dosyanın SHA-256'sı = noteHash mi? path yürünce köke varılıyor mu?
                        (internet gerekmez; tarayıcı da aynısını yapacak)
    verify_on_chain  -> txid'li işlemin OP_RETURN'ünde bu kök gerçekten var mı ve
                        işlem bir blokta mı? (bir Bitcoin node'u gerekir)

ÖNEMLİ: Alan adları sabit sözleşmedir (02 bölüm 6); değişirse JS doğrulayıcı da
(Erdener) değişmeli. NAMESPACE core/ns.py'den (Arda) içe aktarılır.
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone

from core.ns import NAMESPACE  # NP-DECISION(K-001): tek tanım core/ns.py'de; burada elle yazılmaz

from . import merkle, opreturn
from .merkle import PathStep

CONTEXT = {"@vocab": NAMESPACE}


# NP-CONTRACT(02#6): alan adları ve yazımları sabit.
def build_proof(
    note_hash_hex: str,
    path: list[PathStep],
    root_hex: str,
    txid: str,
    block_height: int,
    block_hash: str,
    block_time: int,
    network: str,
) -> dict:
    return {
        "@context": CONTEXT,
        "@type": "Proof",
        "@id": f"{NAMESPACE}proof/{note_hash_hex}",
        "noteHash": note_hash_hex,
        "hashAlgorithm": "SHA-256",
        # Proof sayfasının ağacı aynı kurallarla yeniden kurabilmesi için:
        "leafPrefix": merkle.LEAF_PREFIX.hex(),
        "nodePrefix": merkle.NODE_PREFIX.hex(),
        "merklePath": [{"side": s.side, "sibling": s.sibling.hex()} for s in path],
        "merkleRoot": root_hex,
        "network": network,
        "txid": txid,
        "blockHeight": block_height,
        "blockHash": block_hash,
        "blockTime": datetime.fromtimestamp(block_time, timezone.utc).isoformat(),
    }


def path_of(proof: dict) -> list[PathStep]:
    return [PathStep(s["side"], bytes.fromhex(s["sibling"])) for s in proof["merklePath"]]


# NP-CONTRACT(02#5.5): imza sabit.
def verify_offline(proof: dict, note_file: bytes) -> tuple[bool, str]:
    """Not dosyası + proof ile, internetsiz kontrol. (sonuç, açıklama) döner."""
    file_hash = hashlib.sha256(note_file).hexdigest()
    if file_hash != proof["noteHash"]:
        # Proposal senaryosu: tek karakter değişse bile "kayıtlı dosya değil".
        return False, "Bu dosya kayıtlı dosya değil (hash eşleşmiyor)"
    ok = merkle.verify_path(bytes.fromhex(proof["noteHash"]), path_of(proof), bytes.fromhex(proof["merkleRoot"]))
    if not ok:
        return False, "Merkle path köke ulaşmıyor"
    return True, "Hash ve Merkle path geçerli"


# NP-CONTRACT(02#5.5): imza sabit.
def verify_on_chain(proof: dict, rpc) -> tuple[bool, str]:
    """İşlemi node'dan çekip kökün OP_RETURN'de olduğunu ve işlemin onaylandığını kontrol eder."""
    # Blok hash'ini de veriyoruz: böylece node'da -txindex açık olmasa da işlem bulunur.
    try:
        tx = rpc.call("getrawtransaction", proof["txid"], True, proof["blockHash"])
    except Exception as e:  # RpcError: işlem o blokta yok ya da blok bilinmiyor
        return False, f"İşlem proof'taki blokta bulunamadı ({e})"
    if tx.get("in_active_chain") is False or tx.get("confirmations", 0) < 1:
        return False, "İşlem ana zincirde onaylı değil"
    roots = [opreturn.parse_root(s) for s in opreturn.op_return_outputs(tx)]
    if bytes.fromhex(proof["merkleRoot"]) not in roots:
        return False, "İşlemin OP_RETURN çıktısında bu kök yok"
    return True, "Kök zincirde, işlem onaylı"
