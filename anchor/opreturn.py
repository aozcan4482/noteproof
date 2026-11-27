# NOTEPROOF-FILE
# module:   anchor
# owner:    burak           second: arda
# story:    S2
# contract: 02#5.5 OP_RETURN
# depends:  -
# status:   stable
"""OP_RETURN çıktısı: Merkle kökünü Bitcoin işlemine koyduğumuz yer.

OP_RETURN, harcanamayan ve içine küçük veri koyulabilen bir çıktı türüdür.
Bizim çıktımızın scriptPubKey'i tam olarak 34 byte'tır:

    0x6a        -> OP_RETURN komutu
    0x20        -> "sonraki 32 byte'ı yığına koy" (push 32)
    <32 byte>   -> Merkle kökü

KVKK kuralı (proposal, hedef G4): zincire not içeriği, isim ya da öğrenci
numarası ASLA gitmez; yalnızca 32 byte'lık kök gider. Bu dosyadaki
fonksiyonlar bunu zorunlu kılar ve testler de her OP_RETURN çıktısını bu
kurala göre kontrol eder (Definition of Done: "Only 32-byte roots reach the chain").
"""

from __future__ import annotations

OP_RETURN = 0x6A
PUSH_32 = 0x20
ROOT_SIZE = 32


# NP-CONTRACT(02#5.5): zincire yalnızca 32 byte'lık kök gider (03 bölüm 9).
def build_script(root: bytes) -> bytes:
    """32 byte'lık kökten OP_RETURN scriptPubKey'i üretir."""
    if len(root) != ROOT_SIZE:
        raise ValueError(f"OP_RETURN'e yalnızca 32 byte'lık kök yazılabilir, {len(root)} byte geldi")
    return bytes([OP_RETURN, PUSH_32]) + root


def parse_root(script_hex: str) -> bytes | None:
    """Bir scriptPubKey bizim biçimimizdeyse içindeki kökü döndürür, değilse None."""
    try:
        script = bytes.fromhex(script_hex)
    except ValueError:
        return None
    if len(script) == 2 + ROOT_SIZE and script[0] == OP_RETURN and script[1] == PUSH_32:
        return script[2:]
    return None


def is_op_return(script_hex: str) -> bool:
    return script_hex[:2].lower() == "6a"


def op_return_outputs(decoded_tx: dict) -> list[str]:
    """Bitcoin Core'un decode ettiği bir işlemdeki bütün OP_RETURN scriptlerini (hex) listeler."""
    return [
        vout["scriptPubKey"]["hex"]
        for vout in decoded_tx.get("vout", [])
        if is_op_return(vout["scriptPubKey"]["hex"])
    ]


def tx_holds_only_root(decoded_tx: dict) -> bool:
    """İşlemde tam olarak bir OP_RETURN var mı ve o da yalnızca 32 byte'lık kök mü?

    Para üstü (change) çıktıları normal adres çıktılarıdır; onlar sayılmaz.
    """
    scripts = op_return_outputs(decoded_tx)
    return len(scripts) == 1 and parse_root(scripts[0]) is not None
