# NOTEPROOF-FILE
# module:   tagger
# owner:    aleyna          second: eylem
# story:    S3
# contract: 02#5.2
# depends:  -
# status:   stub
# NP-STUB(owner=eylem, contract=02#5.2): ontology/vocab.py (EYL-3) main'e girince bu dosya silinir.
"""Eylem'in sözlüğünün (ontology/vocab.py, EYL-3) geçici sahtesi; yalnızca tagger testleri için.

İmzalar 02#5.2 ile birebir aynıdır. Gerçek Vocabulary main'e girince bu dosya silinir ve testler
`from ontology.vocab import Vocabulary` ile gerçek sözlüğü kullanır; değişen tek şey içe aktarma satırıdır.

Kimlikler 02#3'teki kalıba ve S5'in kabul kriterindeki hiyerarşiye uyar
(Topic_Transactions > Topic_TransactionFees > Topic_FeeRate). Etiketler geçicidir; gerçek etiketler Eylem'indir.
Topic_TheBlockchain ve Topic_MerkleTrees yalnızca bu testler için uydurulmuş kimliklerdir; gerçek sözlükte
farklı olabilirler. Değerlendirme setinde (manifest.csv) bu dosyadaki kimlikler değil, Eylem'in listesi kullanılır.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Concept:
    id: str
    label_tr: str
    label_en: str
    broader: str | None  # üst kavramın id'si; dersler için None


_CONCEPTS = [
    Concept(
        "Course_SEN0401",
        "Yazılım Mühendisliğinde Özel Konular (Blokzincir)",
        "Special Topics in Software Engineering (Blockchain)",
        None,
    ),
    Concept("Topic_Transactions", "İşlemler", "Transactions", "Course_SEN0401"),
    Concept("Topic_TransactionFees", "İşlem ücretleri", "Transaction fees", "Topic_Transactions"),
    Concept("Topic_FeeRate", "Ücret oranı", "Fee rate", "Topic_TransactionFees"),
    Concept("Topic_TheBlockchain", "Blokzincir", "The blockchain", "Course_SEN0401"),
    Concept("Topic_MerkleTrees", "Merkle ağaçları", "Merkle trees", "Topic_TheBlockchain"),
]


class Vocabulary:
    def __init__(self, concepts: list[Concept]) -> None:
        self._by_id = {c.id: c for c in concepts}

    @classmethod
    def load(cls) -> "Vocabulary":
        return cls(list(_CONCEPTS))

    def courses(self) -> list[Concept]:
        return [c for c in self._by_id.values() if c.broader is None]

    def topics(self, course_id: str) -> list[Concept]:
        return [c for c in self._by_id.values() if c.broader is not None and self._course_of(c.id) == course_id]

    def is_course(self, concept_id: str) -> bool:
        c = self._by_id.get(concept_id)
        return c is not None and c.broader is None

    def is_topic(self, concept_id: str) -> bool:
        c = self._by_id.get(concept_id)
        return c is not None and c.broader is not None

    def narrower(self, topic_id: str) -> list[str]:
        found: list[str] = []
        frontier = [topic_id]
        while frontier:
            parent = frontier.pop()
            for c in self._by_id.values():
                if c.broader == parent and c.id not in found:
                    found.append(c.id)
                    frontier.append(c.id)
        return found

    def as_graph(self):
        raise NotImplementedError("Sahte sözlükte RDF grafiği yok; gerçeği ontology/vocab.py'dedir.")

    def _course_of(self, concept_id: str) -> str | None:
        c = self._by_id.get(concept_id)
        while c is not None and c.broader is not None:
            c = self._by_id.get(c.broader)
        return c.id if c is not None else None
