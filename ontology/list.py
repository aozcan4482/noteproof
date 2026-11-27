# NOTEPROOF-FILE
# module:   ontology
# owner:    eylem           second: aleyna
# story:    S3, S5
# contract: -
# depends:  -
# status:   wip
"""Sözlükteki bütün ders ve konu kimliklerini tablo olarak yazar.

Çalıştırma (repo kökünden): `python -m ontology.list`

Çıktı Markdown tablosudur; PR açıklamasına ve ekip grubuna olduğu gibi yapıştırılabilir (EYL-6).
Tagger istemi (Aleyna), `evalset/manifest.csv` (Emine) ve arama (Erdener) kimlikleri bu listeden alır.
"""

from __future__ import annotations

import sys

from ontology.vocab import Concept, Vocabulary


def render(vocabulary: Vocabulary) -> str:
    """Sözlüğü Markdown tablosu olarak döndürür. Düzey, dersin altındaki derinliktir (ders = 0)."""
    lines = [
        "| Kimlik | Düzey | Üst kavram | Türkçe etiket | İngilizce etiket |",
        "| --- | --- | --- | --- | --- |",
    ]
    for course in vocabulary.courses():
        lines.append(_row(course, 0))
        for topic in vocabulary.topics(course.id):
            lines.append(_row(topic, _depth(vocabulary, topic)))
    return "\n".join(lines)


def _depth(vocabulary: Vocabulary, concept: Concept) -> int:
    depth = 0
    while concept.broader is not None:
        depth += 1
        concept = vocabulary.get(concept.broader)
    return depth


def _row(concept: Concept, depth: int) -> str:
    broader = f"`{concept.broader}`" if concept.broader else "—"
    return f"| `{concept.id}` | {depth} | {broader} | {concept.label_tr} | {concept.label_en} |"


def main() -> int:
    vocabulary = Vocabulary.load()
    print(render(vocabulary))
    topic_count = sum(len(vocabulary.topics(c.id)) for c in vocabulary.courses())
    print(f"\n{len(vocabulary.courses())} ders, {topic_count} konu.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
