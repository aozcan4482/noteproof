# NOTEPROOF-FILE
# module:   evalset
# owner:    emine           second: aleyna
# story:    S3, S6
# contract: manifest.csv sütunları (uyeler/emine.md bölüm 2)
# depends:  -
# status:   stable
"""Değerlendirme setini diskten okuma/yazma."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# NP-CONTRACT(02#3): manifest.csv sütunları sabit; tagger ölçümü (Aleyna, evalset/run_tagger.py) da bunları okur.
MANIFEST_FIELDS = ["id", "course", "topics", "author", "registered_at"]
PLANTED_FIELDS = ["copy_id", "source_id", "transform", "author", "registered_at"]


@dataclass(frozen=True)
class EvalNote:
    id: str
    course: str
    topics: tuple[str, ...]  # SKOS konu kimlikleri; manifest'te ";" ile ayrılır
    author: str  # takma ad (ör. "yazar-03"), gerçek isim DEĞİL
    registered_at: str  # ISO 8601
    text: str


@dataclass(frozen=True)
class PlantedCopy:
    copy_id: str
    source_id: str
    transform: str
    author: str
    registered_at: str
    text: str


def load_notes(root: Path = ROOT) -> list[EvalNote]:
    rows = _read_csv(root / "manifest.csv", MANIFEST_FIELDS)
    return [
        EvalNote(
            r["id"],
            r["course"],
            tuple(t.strip() for t in r["topics"].split(";") if t.strip()),
            r["author"],
            r["registered_at"],
            (root / "notes" / f"{r['id']}.txt").read_text(encoding="utf-8"),
        )
        for r in rows
    ]


def load_planted(root: Path = ROOT) -> list[PlantedCopy]:
    rows = _read_csv(root / "planted" / "planted.csv", PLANTED_FIELDS)
    return [
        PlantedCopy(
            r["copy_id"],
            r["source_id"],
            r["transform"],
            r["author"],
            r["registered_at"],
            (root / "planted" / f"{r['copy_id']}.txt").read_text(encoding="utf-8"),
        )
        for r in rows
    ]


def write_planted(copies: list[PlantedCopy], root: Path = ROOT) -> None:
    d = root / "planted"
    d.mkdir(parents=True, exist_ok=True)
    for old in d.glob("*.txt"):
        old.unlink()
    with open(d / "planted.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, PLANTED_FIELDS)
        w.writeheader()
        for c in copies:
            w.writerow({k: getattr(c, k) for k in PLANTED_FIELDS})
            (d / f"{c.copy_id}.txt").write_text(c.text, encoding="utf-8")


def _read_csv(path: Path, fields: list[str]) -> list[dict]:
    if not path.exists():
        return []
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if rows and set(fields) - set(rows[0]):
        raise ValueError(f"{path}: eksik sütunlar {sorted(set(fields) - set(rows[0]))}")
    return rows
