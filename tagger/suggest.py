# NOTEPROOF-FILE
# module:   tagger
# owner:    aleyna          second: eylem
# story:    S3
# contract: 02#5.3
# depends:  ontology.vocab.Vocabulary
# status:   wip
"""Etiket önerisi: notun metninden, sözlükteki bir ders, konular ve iki cümlelik özet önerir.

Proposal'daki aktivite modelinde adım 4a; story S3: "Transaction fee notu yüklenince AI, SEN0401 dersini
ve sözlükten 'Transaction fees' konusunu önerir; yazar onaylayana kadar hiçbir şey kaydedilmez."

Akış:
1. İstem, her çağrıda Vocabulary'den üretilir (elle yazılmış konu listesi yok). Böylece Eylem sözlüğe
   konu eklediğinde tagger kendiliğinden onu da görür.
2. Model bir JSON nesnesi döndürür: {"course": ..., "topics": [...], "summary": ...}.
3. Yanıt kodla süzülür: sözlükte olmayan ders ya da konu kimliği çıktıya giremez (02#5.3). Modelin
   "uydurduğu" bir kimlik, kayıt servisinde SHACL ihlaline (S4) dönüşmeden burada düşer.
4. Bozuk ya da beklenmeyen yanıt hata değil, boş öneridir: yazar dersi ve konuları listeden kendisi seçer.

Bu modül hiçbir şey kaydetmez: diske, grafiğe ya da günlüğe yazmaz. Not içeriği günlüğe hiç yazılmaz.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import TYPE_CHECKING

from .llm import LLMClient, client_from_env

if TYPE_CHECKING:
    # Yalnızca tip denetimi için: suggest sözlüğü parametre olarak alır, tagger çalışırken rdflib'i
    # içe aktarmak zorunda kalmaz. Testler gerçek sözlüğü (ontology.vocab, EYL-3) kullanır.
    from ontology.vocab import Vocabulary


# NP-CONTRACT(02#5.3): alan adları ve türleri sabit; kayıt servisi (Arda) önizleme yanıtına bunları koyar.
@dataclass(frozen=True)
class TagSuggestion:
    course: str | None  # "Course_SEN0401" ya da None
    topics: list[str]  # yalnızca sözlükteki "Topic_*" kimlikleri; boş olabilir
    summary: str  # iki cümle, notun dilinde


SYSTEM_PROMPT = (
    "Sen öğrencilerin ders notlarını etiketleyen bir yardımcısın. Notu oku ve aşağıdaki sözlükten "
    "notun dersini ve konularını seç. Yalnızca sözlükte yazan kimlikleri kullan; yeni kimlik uydurma. "
    "Notun dersini bulamıyorsan course için null, topics için boş liste döndür. "
    "Notu iki cümleyle, notun yazıldığı dilde özetle. "
    "Yanıtın yalnızca şu biçimde tek bir JSON nesnesi olsun: "
    '{"course": "...", "topics": ["..."], "summary": "..."}'
)


def build_prompt(text: str, vocabulary: Vocabulary) -> str:
    """Modele gönderilecek istemi kurar: sözlük (kimlik ve iki dilde etiket) ve notun metni."""
    lines = ["SÖZLÜK", "Dersler ve konuları (kimlik | Türkçe etiket | İngilizce etiket | üst kavram):"]
    for course in vocabulary.courses():
        lines.append(f"- {course.id} | {course.label_tr} | {course.label_en}")
        for topic in vocabulary.topics(course.id):
            lines.append(f"    - {topic.id} | {topic.label_tr} | {topic.label_en} | {topic.broader}")
    lines += ["", "NOT", text.strip()]
    return "\n".join(lines)


# NP-CONTRACT(02#5.3): imza sabit. Hiçbir şey kaydetmez; sözlükte olmayan kimliği asla döndürmez.
def suggest(text: str, vocabulary: Vocabulary, llm: LLMClient | None = None) -> TagSuggestion:
    """Notun metni için ders, konu ve özet önerisi döndürür.

    llm verilmezse istemci ortam değişkenlerinden kurulur (client_from_env). Testler her zaman FakeLLM verir.
    """
    if not text or not text.strip():
        # NP-TODO(arda): metni çıkmayan dosyada önizleme bu hatayı yakalayıp yazara "metin okunamadı" demeli.
        raise ValueError("Not metni boş; öneri üretilemez.")
    if not vocabulary.courses():
        raise ValueError("Sözlükte hiç ders yok; öneri üretilemez.")

    client = llm if llm is not None else client_from_env()
    answer = client.complete(build_prompt(text, vocabulary), system=SYSTEM_PROMPT)
    return _filter(_parse(answer), vocabulary)


def _parse(answer: str) -> dict:
    """Model yanıtındaki JSON nesnesini çıkarır; bulamazsa boş sözlük döner (hata değil)."""
    if not isinstance(answer, str):
        return {}
    # Modeller JSON'u bazen ```json ... ``` bloğuna ya da açıklama cümlelerinin arasına koyar:
    # ilk "{" ile son "}" arasını almak ikisini de kapsar.
    start, end = answer.find("{"), answer.rfind("}")
    if start == -1 or end <= start:
        return {}
    try:
        data = json.loads(answer[start : end + 1])
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def _filter(data: dict, vocabulary: Vocabulary) -> TagSuggestion:
    """Yanıtı sözlüğe göre süzer: geçersiz ders -> ders ve konu yok; dersin dışındaki konular düşer."""
    course = data.get("course")
    if not isinstance(course, str) or not vocabulary.is_course(course):
        # Ders yoksa konu da önerilmez: konu her zaman bir derse bağlıdır (02#4). Tahmin uydurma.
        return TagSuggestion(course=None, topics=[], summary=_summary(data))

    allowed = {t.id for t in vocabulary.topics(course)}
    raw_topics = data.get("topics")
    topics: list[str] = []
    for topic in raw_topics if isinstance(raw_topics, list) else []:
        if isinstance(topic, str) and topic in allowed and topic not in topics:
            topics.append(topic)
    return TagSuggestion(course=course, topics=topics, summary=_summary(data))


def _summary(data: dict) -> str:
    summary = data.get("summary")
    return summary.strip() if isinstance(summary, str) else ""
