# NOTEPROOF-FILE
# module:   anchor
# owner:    burak           second: arda
# story:    S2, S7
# contract: 02#5.5 Merkle kuralları, 02#6 proof dosyası
# depends:  -
# status:   stable
"""Ortak test vektörleri: Python ve tarayıcı aynı Merkle kurallarını uyguluyor mu?

Proof sayfası (Erdener, `web/js/verify.js`) bir notun kanıtını tarayıcıda, bizim Python kodumuzdan bağımsız
olarak doğrular. İkisinin aynı sonucu verdiğini göstermenin yolu, ikisine de AYNI girdileri ve beklenen
sonuçları vermektir. Bu modül o girdileri üretir:

    python -m anchor.vectors            # tests/vectors/ altındaki üç dosyayı yeniden yazar

Üretilen dosyalar (BRK-3):
    tests/vectors/merkle_vectors.json   1, 2, 3, 5 ve 8 yapraklı ağaçlar: her yaprağın path'i ve kökü (beklenen
                                        true) ile bozulmuş path, yanlış kök ve yanlış taraf örnekleri (beklenen false)
    tests/vectors/sample_note.txt       sentetik bir ders notu (gerçek öğrenci notu değil, kişisel veri yok)
    tests/vectors/sample_proof.json     o notun proof dosyası; alanları 02 bölüm 6 ile birebir aynı

Çıktı her çalıştırmada byte byte aynıdır (rastgelelik yok), böylece dosyalar repoda sabit kalır.
`tests/anchor/test_vectors.py` dosyaların bu modülün çıktısıyla aynı olduğunu da denetler.

Satır sonları: repo kökündeki `.gitattributes` dosyasında `tests/vectors/* -text` var. Windows'ta Git
satır sonlarını değiştirseydi `sample_note.txt`'nin SHA-256'sı ve dolayısıyla bütün proof değişirdi.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from . import merkle
from .merkle import PathStep
from .proof import build_proof

LEAF_COUNTS = [1, 2, 3, 5, 8]
DEFAULT_OUT = Path("tests/vectors")

SAMPLE_NOTE = (
    "SEN0401 - Transaction fees (örnek not, sentetik)\n"
    "\n"
    "Bir işlemin ücreti, girdilerin toplamı ile çıktıların toplamı arasındaki farktır.\n"
    "Madenciler ücret oranı (sat/vB) yüksek işlemleri önce bloğa alır.\n"
    "Ücret düşük kalırsa işlem RBF ile daha yüksek ücretle yeniden gönderilebilir.\n"
)

# Örnek proof'un zincir alanları. Bu proof yalnızca ÇEVRİMDIŞI doğrulama (hash + Merkle path) için vardır;
# zincirde böyle bir işlem yoktur. Ağ "regtest" yazılır: proof sayfası regtest'te zincir kontrolü yapmaz
# (K-008), yani bu sahte değerler hiçbir zaman gerçek bir işlem gibi gösterilmez.
SAMPLE_NETWORK = "regtest"
SAMPLE_BLOCK_HEIGHT = 101
SAMPLE_BLOCK_TIME = 1_764_288_000  # 2025-11-28T00:00:00Z
SAMPLE_INDEX = 2  # örnek not, 5 yapraklı ağacın 3. yaprağı: path'inde hem sol hem sağ kardeş olur


def _sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def note_hashes(count: int) -> list[str]:
    """Sabit, tekrarlanabilir not hash'leri: "noteproof-vector-0", "-1", ... metinlerinin SHA-256'sı."""
    return [_sha256_hex(f"noteproof-vector-{i}".encode()) for i in range(count)]


def _path_json(path: list[PathStep]) -> list[dict]:
    # NP-CONTRACT(02#6): proof dosyasındaki merklePath ile aynı biçim: {"side": "left|right", "sibling": hex}
    return [{"side": s.side, "sibling": s.sibling.hex()} for s in path]


def _flip_first_byte(hex_value: str) -> str:
    """Bir hash'in ilk byte'ını değiştirir; bozulmuş girdi üretmek için."""
    first = int(hex_value[:2], 16) ^ 0xFF
    return f"{first:02x}{hex_value[2:]}"


def build_merkle_vectors() -> dict:
    trees = []
    negative = []
    for count in LEAF_COUNTS:
        hashes = note_hashes(count)
        root, paths = merkle.build_tree([bytes.fromhex(h) for h in hashes])
        proofs = [
            {"index": i, "noteHash": h, "merklePath": _path_json(p), "expected": True}
            for i, (h, p) in enumerate(zip(hashes, paths))
        ]
        trees.append({"leafCount": count, "noteHashes": hashes, "merkleRoot": root.hex(), "proofs": proofs})

        # Reddedilmesi gereken örnekler. Path'i olmayan tek yapraklı ağaçta yalnızca yanlış kök denenebilir.
        last = count - 1
        good_path = _path_json(paths[last])
        negative.append({
            "name": f"wrong-root-{count}",
            "noteHash": hashes[last],
            "merklePath": good_path,
            "merkleRoot": _flip_first_byte(root.hex()),
            "expected": False,
        })
        if good_path:
            tampered = [dict(good_path[0], sibling=_flip_first_byte(good_path[0]["sibling"]))] + good_path[1:]
            negative.append({
                "name": f"tampered-sibling-{count}",
                "noteHash": hashes[last],
                "merklePath": tampered,
                "merkleRoot": root.hex(),
                "expected": False,
            })
            other = "right" if good_path[0]["side"] == "left" else "left"
            wrong_side = [dict(good_path[0], side=other)] + good_path[1:]
            negative.append({
                "name": f"wrong-side-{count}",
                "noteHash": hashes[last],
                "merklePath": wrong_side,
                "merkleRoot": root.hex(),
                "expected": False,
            })

    return {
        "description": (
            "NoteProof Merkle test vectors (BRK-3). Generated by `python -m anchor.vectors`; do not edit by hand. "
            "Leaf hash = SHA256(leafPrefix || noteHash), node hash = SHA256(nodePrefix || left || right); "
            "an unpaired node moves up unchanged. A step with side \"left\" means hash(sibling, current); "
            "\"right\" means hash(current, sibling)."
        ),
        "hashAlgorithm": "SHA-256",
        "leafPrefix": merkle.LEAF_PREFIX.hex(),
        "nodePrefix": merkle.NODE_PREFIX.hex(),
        "trees": trees,
        "negative": negative,
    }


def build_sample_proof() -> dict:
    """Örnek notun, 5 yapraklı bir ağaçtaki proof'u. Diğer yapraklar merkle_vectors'daki hash'lerdir."""
    note_hash = _sha256_hex(SAMPLE_NOTE.encode())
    hashes = note_hashes(5)
    hashes[SAMPLE_INDEX] = note_hash
    root, paths = merkle.build_tree([bytes.fromhex(h) for h in hashes])
    # Sahte ama tekrarlanabilir zincir değerleri (yukarıdaki SAMPLE_* açıklamasına bakın).
    txid = _sha256_hex(b"noteproof-sample-txid")
    block_hash = _sha256_hex(b"noteproof-sample-block")
    return build_proof(
        note_hash, paths[SAMPLE_INDEX], root.hex(), txid,
        SAMPLE_BLOCK_HEIGHT, block_hash, SAMPLE_BLOCK_TIME, SAMPLE_NETWORK,
    )


def render() -> dict[str, bytes]:
    """Üç dosyanın içeriği, dosya adına göre. Yazmadan karşılaştırmak için testler de bunu kullanır."""
    def as_json(data: dict) -> bytes:
        return (json.dumps(data, indent=2, ensure_ascii=False) + "\n").encode()

    return {
        "merkle_vectors.json": as_json(build_merkle_vectors()),
        "sample_note.txt": SAMPLE_NOTE.encode(),
        "sample_proof.json": as_json(build_sample_proof()),
    }


def write(out_dir: Path = DEFAULT_OUT) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for name, content in render().items():
        path = out_dir / name
        path.write_bytes(content)  # write_bytes: satır sonları işletim sistemine göre değişmez
        written.append(path)
    return written


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="NoteProof Merkle test vektörlerini üretir (BRK-3)")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT, help="çıktı klasörü (varsayılan tests/vectors)")
    args = parser.parse_args(argv)
    for path in write(args.out):
        print(f"yazıldı: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
