"""Planted copy üretici: kaynak notlardan, gerçek hayattaki kopyalara benzeyen 20 kopya.

Her kopya, kaynağından SONRA ve BAŞKA bir takma adlı hesapla kaydedilmiş sayılır.
Dönüşümler (TRANSFORMS) proposal'daki senaryoyu karşılar: "a note nearly identical
to one registered a week earlier by another student".

Seed sabit olduğu için aynı notlardan her zaman aynı kopyalar çıkar.

Çalıştırma (repo kökünden):
    python -m evalset.plant            # evalset/planted/ klasörünü yeniden üretir
"""

from __future__ import annotations

import argparse
import random
import re
from datetime import datetime, timedelta

from .data import ROOT, EvalNote, PlantedCopy, load_notes, write_planted

N_COPIES = 20
SEED = 401  # SEN0401

_SENT = re.compile(r"(?<=[.!?])\s+")
_OCR = {"i": "l", "l": "1", "o": "0", "e": "c", "a": "o", "m": "rn", "ı": "i", "ş": "s", "ğ": "g"}
_TR_ASCII = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")


def _sentences(t: str) -> list[str]:
    return [s for s in _SENT.split(t.strip()) if s]


def reformat(t: str, r: random.Random) -> str:
    """Aynı metin, farklı satır sonu/boşluk/büyük harf: hash değişir, içerik değişmez."""
    return "\n".join(s.upper() if r.random() < 0.2 else s for s in _sentences(t)) + "\n"


def ocr_noise(t: str, r: random.Random) -> str:
    """Fotoğraftan OCR ile çıkarılmış gibi: harflerin ~%4'ü yanlış okunmuş."""
    return "".join(_OCR[c] if c in _OCR and r.random() < 0.04 else c for c in t)


def ascii_fold(t: str, r: random.Random) -> str:
    """Türkçe karakterleri silinmiş (WhatsApp'tan elle yazılmış gibi)."""
    return t.translate(_TR_ASCII)


def reorder(t: str, r: random.Random) -> str:
    """Cümle sırası karıştırılmış."""
    s = _sentences(t)
    r.shuffle(s)
    return " ".join(s)


def drop_some(t: str, r: random.Random) -> str:
    """Cümlelerin ~%25'i silinmiş (ama en az 3 cümle kalır)."""
    s = _sentences(t)
    keep = [x for x in s if r.random() > 0.25]
    return " ".join(keep if len(keep) >= 3 else s[:3])


def add_own(t: str, r: random.Random, other: str = "") -> str:
    """Başka bir notun birkaç cümlesi eklenmiş: kopya + 'kendi katkısı'."""
    extra = _sentences(other)[:2] if other else ["Bu konu sınavda çıkabilir, tekrar et."]
    return " ".join(_sentences(t) + extra)


def mixed(t: str, r: random.Random) -> str:
    """Birkaç dönüşüm birden: sıra + silme + OCR."""
    return ocr_noise(drop_some(reorder(t, r), r), r)


TRANSFORMS = {
    "reformat": reformat,
    "ocr_noise": ocr_noise,
    "ascii_fold": ascii_fold,
    "reorder": reorder,
    "drop_some": drop_some,
    "add_own": add_own,
    "mixed": mixed,
}


def plant(notes: list[EvalNote], n: int = N_COPIES, seed: int = SEED) -> list[PlantedCopy]:
    if not notes:
        return []
    r = random.Random(seed)
    names = list(TRANSFORMS)
    sources = r.sample(notes, n) if len(notes) >= n else [notes[i % len(notes)] for i in range(n)]
    authors = sorted({x.author for x in notes})
    out = []
    for i, src in enumerate(sources):
        name = names[i % len(names)]
        fn = TRANSFORMS[name]
        if name == "add_own":
            other = r.choice([x for x in notes if x.id != src.id] or [src])
            text = fn(src.text, r, other.text)
        else:
            text = fn(src.text, r)
        # Kopyalayan: kaynağın yazarı dışında biri; bir hafta sonra kaydediyor.
        copier = f"kopyalayan-{i + 1:02d}" if len(authors) < 2 else r.choice([a for a in authors if a != src.author])
        when = (datetime.fromisoformat(src.registered_at) + timedelta(days=7)).isoformat()
        out.append(PlantedCopy(f"copy-{i + 1:02d}", src.id, name, copier, when, text))
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--n", type=int, default=N_COPIES)
    ap.add_argument("--seed", type=int, default=SEED)
    a = ap.parse_args(argv)
    notes = load_notes(ROOT)
    if not notes:
        print("evalset/manifest.csv boş ya da yok: önce notları ekleyin (evalset/README.md).")
        return 1
    copies = plant(notes, a.n, a.seed)
    write_planted(copies, ROOT)
    print(f"{len(copies)} planted copy yazıldı: {ROOT / 'planted'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
