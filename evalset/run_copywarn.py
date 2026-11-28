# NOTEPROOF-FILE
# module:   evalset
# owner:    emine           second: aleyna
# story:    S6
# contract: -
# depends:  copywarn.CopyChecker.add, copywarn.CopyChecker.check
# status:   stable
"""Kopya uyarısını değerlendirme setiyle ölçer (objective O5, story S6).

Ölçülenler:
  recall          -> 20 planted copy'den kaçı DOĞRU kaynağa bağlanarak işaretlendi (hedef >= %90)
  false_positives -> özgün notlardan kaçı yanlışlıkla "kopya" sayıldı (bilgi amaçlı, CI'yı kırmaz)

Notlar kayıt zamanına göre sırayla arşive "kaydedilir"; her not yalnızca kendinden
önce kaydedilmiş notlarla karşılaştırılır — gerçek sistemde olduğu gibi.

Çalıştırma (repo kökünden):
    python -m evalset.run_copywarn                 # rapor yazdırır, hedefin altındaysa çıkış kodu 1
    python -m evalset.run_copywarn --json rapor.json
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

from copywarn import CopyChecker, RegisteredNote
from copywarn.checker import DEFAULT_THRESHOLD

from .data import ROOT, EvalNote, PlantedCopy, load_notes, load_planted

TARGET_RECALL = 0.90  # proposal, objective "Planted copies caught by the copy warning": 90


@dataclass
class Report:
    notes: int
    copies: int
    caught: int
    recall: float
    target: float
    passed: bool
    threshold: float
    false_positives: list[dict] = field(default_factory=list)
    missed: list[dict] = field(default_factory=list)
    by_transform: dict[str, list[int]] = field(default_factory=dict)  # dönüşüm -> [yakalanan, toplam]


def evaluate(notes: list[EvalNote], copies: list[PlantedCopy], threshold: float = DEFAULT_THRESHOLD, target: float = TARGET_RECALL) -> Report:
    checker = CopyChecker(threshold)
    fps = []
    # Özgün notları kayıt sırasıyla ekle; her biri kendinden öncekilerle karşılaştırılır.
    for n in sorted(notes, key=lambda x: x.registered_at):
        w = checker.check(n.text, author=n.author, before=n.registered_at)
        if w:
            fps.append({"note": n.id, "flagged_as_copy_of": w[0].earlier_note_id, "score": w[0].score})
        checker.add(RegisteredNote(n.id, n.text, n.author, n.registered_at))

    caught, missed, by = 0, [], {}
    for c in copies:
        w = checker.check(c.text, author=c.author, before=c.registered_at)
        ok = any(x.earlier_note_id == c.source_id for x in w)
        caught += ok
        t = by.setdefault(c.transform, [0, 0])
        t[0] += ok
        t[1] += 1
        if not ok:
            best = checker.score(c.text, next(n.text for n in notes if n.id == c.source_id))
            missed.append({"copy": c.copy_id, "source": c.source_id, "transform": c.transform, "score_vs_source": round(best[0], 4)})

    recall = caught / len(copies) if copies else 0.0
    return Report(len(notes), len(copies), caught, round(recall, 4), target, bool(copies) and recall >= target, threshold, fps, missed, by)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Kopya uyarısını değerlendirme setiyle ölç")
    ap.add_argument("--root", type=Path, default=ROOT)
    ap.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD)
    ap.add_argument("--json", type=Path, help="raporu bu dosyaya da yaz")
    a = ap.parse_args(argv)

    notes, copies = load_notes(a.root), load_planted(a.root)
    if not notes or not copies:
        print("Değerlendirme seti henüz boş: evalset/README.md'deki adımları izleyin.")
        return 1
    r = evaluate(notes, copies, a.threshold)
    print(f"Kopya uyarısı: {r.caught}/{r.copies} planted copy yakalandı = %{100 * r.recall:.0f} (hedef %{100 * r.target:.0f}) -> {'GEÇTİ' if r.passed else 'KALDI'}")
    for t, (k, n) in sorted(r.by_transform.items()):
        print(f"  {t:<10} {k}/{n}")
    print(f"Yanlış alarm (özgün notlar): {len(r.false_positives)}/{r.notes}")
    for m in r.missed:
        print(f"  kaçan: {m}")
    if a.json:
        a.json.write_text(json.dumps(asdict(r), ensure_ascii=False, indent=1), encoding="utf-8")
    return 0 if r.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
