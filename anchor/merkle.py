# NOTEPROOF-FILE
# module:   anchor
# owner:    burak           second: arda
# story:    S2, S7
# contract: 02#5.5 Merkle kuralları
# depends:  -
# status:   stable
"""Merkle tree: günün not hash'lerinden tek bir 32 byte'lık kök üretir.

Neden Merkle tree?
    Her not için ayrı bir Bitcoin işlemi pahalı olurdu. Bunun yerine günün bütün
    hash'lerini bir ağaçta birleştirip yalnızca kökü zincire yazıyoruz (Nakamoto,
    bölüm 7). Her not kendi "Merkle path"ini (yolunu) alır: yapraktan köke kadar
    yanındaki kardeş hash'lerin listesi. Bu yol + kök, notun o gün ağaçta
    olduğunu kanıtlar.

Tasarım kararları (proof sayfası da AYNI kuralları kullanmak zorunda):
    * Yaprak hash'i:   SHA256(0x00 || not_hash)
    * İç düğüm hash'i: SHA256(0x01 || sol || sağ)
      0x00 / 0x01 önekleri yaprak ile iç düğümü birbirinden ayırır. Böylece biri
      iki hash'i birleştirip "sahte yaprak" gibi gösteremez (second-preimage
      saldırısı). Aynı yaklaşım RFC 6962'de (Certificate Transparency) var.
    * Tek sayıda düğüm kalırsa son düğüm kopyalanmaz, olduğu gibi bir üst
      seviyeye çıkar. Bitcoin'in "sonuncuyu kopyala" kuralı CVE-2012-2459
      açığına yol açmıştı; biz onu kullanmıyoruz.
    * Hash'ler tek SHA-256'dır (Bitcoin'deki gibi çift değil); kanıt için yeterli.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

# NP-CONTRACT(02#5.5): Merkle kuralları sabit; web/js/verify.js ve tests/vectors/ aynısını kullanır.
LEAF_PREFIX = b"\x00"
NODE_PREFIX = b"\x01"
HASH_SIZE = 32  # SHA-256 çıktısı 32 byte


def sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def hash_leaf(note_hash: bytes) -> bytes:
    """Notun SHA-256 hash'ini ağacın yaprağına çevirir."""
    return sha256(LEAF_PREFIX + note_hash)


def hash_node(left: bytes, right: bytes) -> bytes:
    """İki çocuk düğümden üst düğümü hesaplar."""
    return sha256(NODE_PREFIX + left + right)


@dataclass(frozen=True)
class PathStep:
    """Merkle path'in bir adımı.

    side: kardeş düğümün hangi tarafta olduğu ("left" ya da "right").
          "left" ise  üst = hash_node(kardeş, şimdiki)
          "right" ise üst = hash_node(şimdiki, kardeş)
    sibling: kardeş düğümün 32 byte'lık hash'i.
    """

    side: str
    sibling: bytes


def _check_hashes(note_hashes: list[bytes]) -> None:
    if not note_hashes:
        raise ValueError("Boş listeden Merkle tree kurulamaz")
    for h in note_hashes:
        if len(h) != HASH_SIZE:
            raise ValueError(f"Her not hash'i 32 byte olmalı, {len(h)} byte geldi")


# NP-CONTRACT(02#5.5): tek kalan düğüm kopyalanmadan yukarı taşınır.
def build_levels(note_hashes: list[bytes]) -> list[list[bytes]]:
    """Ağacın bütün seviyelerini aşağıdan yukarı döndürür.

    levels[0] yapraklar, levels[-1] ise tek elemanlı kök seviyesidir.
    """
    _check_hashes(note_hashes)
    level = [hash_leaf(h) for h in note_hashes]
    levels = [level]
    while len(level) > 1:
        parent: list[bytes] = []
        for i in range(0, len(level), 2):
            if i + 1 < len(level):
                parent.append(hash_node(level[i], level[i + 1]))
            else:
                # Eşi olmayan son düğüm: kopyalamadan yukarı taşı.
                parent.append(level[i])
        levels.append(parent)
        level = parent
    return levels


def _path_from_levels(levels: list[list[bytes]], index: int) -> list[PathStep]:
    path: list[PathStep] = []
    for level in levels[:-1]:  # kök seviyesinde kardeş yok
        if index % 2 == 0:
            # Biz soldayız; sağımızda kardeş varsa ekle. Yoksa yukarı taşındık,
            # bu seviyede adım yok.
            if index + 1 < len(level):
                path.append(PathStep("right", level[index + 1]))
        else:
            path.append(PathStep("left", level[index - 1]))
        index //= 2
    return path


def merkle_root(note_hashes: list[bytes]) -> bytes:
    """Zincire yazılacak 32 byte'lık kök."""
    return build_levels(note_hashes)[-1][0]


def merkle_path(note_hashes: list[bytes], index: int) -> list[PathStep]:
    """Tek bir notun (index sıradaki) Merkle path'i."""
    if not 0 <= index < len(note_hashes):
        raise IndexError(index)
    return _path_from_levels(build_levels(note_hashes), index)


def build_tree(note_hashes: list[bytes]) -> tuple[bytes, list[list[PathStep]]]:
    """Kökü ve bütün notların path'lerini tek seferde hesaplar (günlük iş bunu kullanır)."""
    levels = build_levels(note_hashes)
    paths = [_path_from_levels(levels, i) for i in range(len(note_hashes))]
    return levels[-1][0], paths


def verify_path(note_hash: bytes, path: list[PathStep], root: bytes) -> bool:
    """Not hash'inden başlayıp path'i yürür; sonuç kök ile aynıysa kanıt geçerlidir."""
    if len(note_hash) != HASH_SIZE or len(root) != HASH_SIZE:
        return False
    current = hash_leaf(note_hash)
    for step in path:
        if step.side == "left":
            current = hash_node(step.sibling, current)
        elif step.side == "right":
            current = hash_node(current, step.sibling)
        else:
            return False
    return current == root
