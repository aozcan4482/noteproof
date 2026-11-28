# NOTEPROOF-FILE
# module:   evalset (yalnızca bu dosya; evalset/'in geri kalanı Emine'nin)
# owner:    aleyna          second: emine
# story:    S3
# contract: 02#3, 02#5.3
# depends:  tagger.suggest.suggest, tagger.llm.client_from_env, ontology.vocab.Vocabulary, evalset.data.load_notes
# status:   stable
"""AI tagger'ı değerlendirme setiyle ölçer (objective O3, story S3).

Ölçü: önerilen konulardan, manifest.csv'de o not için bilinen konular arasında olanların oranı
(hedef >= %80). Ders önerisinin doğruluğu bilgi amaçlı raporlanır, sonucu değiştirmez.

Her not için suggest() çağrılır; dil modeline yalnızca not metni gider. Rapora ve ekrana not metni,
model özeti ya da API anahtarı yazılmaz; yalnızca not kimlikleri, konu kimlikleri ve sayılar.

Çalıştırma (repo kökünden; .env değişkenleri ortama yüklenmiş olmalı):
    set -a; . ./.env; set +a
    python -m evalset.run_tagger                  # rapor yazdırır, hedefin altındaysa çıkış kodu 1
    python -m evalset.run_tagger --json rapor.json

API anahtarı (NOTEPROOF_LLM_API_KEY) yoksa ölçüm "atlandı" notuyla çıkış kodu 0 verir: CI'da secret
olmayan bir fork ya da PR kırmızıya dönmez (uyeler/aleyna.md, ALY-5). Set boşsa çıkış kodu 1.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Callable

from tagger.llm import ENV_API_KEY, LLMClient, client_from_env
from tagger.suggest import suggest

from .data import ROOT, EvalNote, load_notes

if TYPE_CHECKING:
    from ontology.vocab import Vocabulary

TARGET = 0.80  # 01_PROJE.md, O3: "≥ %80"

# Groq ücretsiz planı kısa sürede çok istekte HTTP 429 veriyor (ALY-R2). Çağrılar arasında beklenir;
# GroqClient ayrıca 429'da kendisi bekleyip yeniden dener.
DEFAULT_DELAY = 2.5


@dataclass
class Report:
    notes: int
    suggested: int  # önerilen konu sayısı (bütün notlarda)
    correct: int  # bunlardan manifest'te bilinen konular arasında olanlar
    precision: float
    target: float
    passed: bool
    course_correct: int  # dersi doğru önerilen not sayısı (bilgi amaçlı)
    no_topic: list[str] = field(default_factory=list)  # hiç konu önerilmeyen notlar
    errors: list[dict] = field(default_factory=list)  # öneri alınamayan notlar
    per_note: list[dict] = field(default_factory=list)


def evaluate(
    notes: list[EvalNote],
    vocabulary: Vocabulary,
    llm: LLMClient,
    *,
    target: float = TARGET,
    delay: float = 0.0,
    sleep: Callable[[float], None] = time.sleep,
) -> Report:
    """Her not için öneriyi üretir ve manifest'teki bilinen konularla karşılaştırır."""
    suggested = correct = course_correct = 0
    no_topic: list[str] = []
    errors: list[dict] = []
    per_note: list[dict] = []

    for i, note in enumerate(notes):
        if i and delay:
            sleep(delay)
        try:
            s = suggest(note.text, vocabulary, llm)
        except (RuntimeError, ValueError) as err:
            # Hata mesajında not metni ya da anahtar yok (tagger/llm.py, tagger/suggest.py).
            errors.append({"note": note.id, "error": str(err)})
            continue

        known = set(note.topics)
        hits = [t for t in s.topics if t in known]
        suggested += len(s.topics)
        correct += len(hits)
        course_correct += s.course == note.course
        if not s.topics:
            no_topic.append(note.id)
        per_note.append(
            {
                "note": note.id,
                "known": sorted(known),
                "suggested": s.topics,
                "correct": hits,
                "course_ok": s.course == note.course,
            }
        )

    precision = correct / suggested if suggested else 0.0
    passed = bool(suggested) and not errors and precision >= target
    return Report(len(notes), suggested, correct, round(precision, 4), target, passed, course_correct,
                  no_topic, errors, per_note)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="AI tagger'ı değerlendirme setiyle ölç (O3)")
    ap.add_argument("--root", type=Path, default=ROOT)
    ap.add_argument("--json", type=Path, help="raporu bu dosyaya da yaz")
    ap.add_argument("--delay", type=float, default=DEFAULT_DELAY, help="çağrılar arası bekleme (sn)")
    a = ap.parse_args(argv)

    notes = load_notes(a.root)
    if not notes:
        print("Değerlendirme seti boş: evalset/manifest.csv'de not yok (EMN-2). Ölçüm yapılamadı.")
        return 1

    if not os.environ.get(ENV_API_KEY, "").strip():
        # GitHub Actions bu satırı uyarı kutusu olarak gösterir; yerelde düz metin olarak görünür.
        print(f"::notice::{ENV_API_KEY} yok; tagger ölçümü atlandı (ALY-5).")
        return 0

    from ontology.vocab import Vocabulary  # rdflib yalnızca ölçüm gerçekten yapılacaksa gerekir

    try:
        llm = client_from_env()
    except RuntimeError as err:
        print(f"Dil modeli kurulamadı: {err}")
        return 1

    report = evaluate(notes, Vocabulary.load(), llm, delay=a.delay)
    _print(report)
    if a.json:
        a.json.write_text(json.dumps(asdict(report), ensure_ascii=False, indent=2), encoding="utf-8")
    return 0 if report.passed else 1


def _print(r: Report) -> None:
    verdict = "GEÇTİ" if r.passed else "KALDI"
    print(f"Tagger ölçümü (O3): {r.correct}/{r.suggested} önerilen konu doğru = %{r.precision * 100:.1f} "
          f"(hedef %{r.target * 100:.0f}) -> {verdict}")
    print(f"Not: {r.notes} · ders doğru: {r.course_correct} · konu önerilmeyen: {len(r.no_topic)} "
          f"· hata: {len(r.errors)}")
    for row in r.per_note:
        wrong = [t for t in row["suggested"] if t not in row["correct"]]
        if wrong:
            print(f"  {row['note']}: bilinen {', '.join(row['known'])} · yanlış öneri {', '.join(wrong)}")
    for e in r.errors:
        print(f"  {e['note']}: HATA {e['error']}")


if __name__ == "__main__":
    sys.exit(main())
