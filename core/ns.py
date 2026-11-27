# NOTEPROOF-FILE
# module:   core
# owner:    arda            second: burak
# story:    -
# contract: 02#3 IRI şeması, 02#5.1 core/ns.py
# depends:  -
# status:   stable
"""NoteProof namespace'i ve IRI üreticiler.

Namespace yalnızca burada tanımlıdır; başka hiçbir dosyada elle yazılmaz (02 bölüm 3). Böylece K-001
kararı değişirse değişiklik tek satır olur. IRI'ler 02 bölüm 3'teki şemayı birebir izler.

Üreticiler girdiyi denetler: geçersiz bir hash ya da kimlikle sessizce yanlış bir IRI üretmek yerine
ValueError verir (03 bölüm 5). Yanlış bir IRI grafiğe bir kez yazılırsa proof'lar ve aramalar onu bulamaz.
"""

from __future__ import annotations

import re
from urllib.parse import quote

# NP-DECISION(K-001): geçici değer; anchor/proof.py (Burak) aynı değeri kullanır. Proof dosyaları
# üretildikten sonra değiştirilmez, karar signet'teki ilk gerçek timestamp'ten önce verilmelidir.
# NP-CONTRACT(02#5.1): ad ve değer sabit.
NAMESPACE: str = "https://github.com/aozcan4482/noteproof/ns#"

# Not hash'i ve txid: küçük harfli 64 karakterlik hex (02 bölüm 3). Büyük harf kabul edilmez, çünkü
# aynı not iki farklı IRI ile grafiğe girerdi.
_HEX64 = re.compile(r"[0-9a-f]{64}")

# Ders ve konu yerel kimlikleri: Course_SEN0401, Topic_TransactionFees (02 bölüm 3).
_CONCEPT_ID = re.compile(r"(Course|Topic)_[A-Za-z0-9]+")


def _check_hex64(value: str, what: str) -> str:
    if not isinstance(value, str) or not _HEX64.fullmatch(value):
        raise ValueError(f"{what} küçük harfli 64 karakterlik hex olmalı: {value!r}")
    return value


# NP-CONTRACT(02#5.1): imza sabit.
def note_iri(note_hash: str) -> str:
    """Notun IRI'si: {NS}note/{hash}."""
    return f"{NAMESPACE}note/{_check_hex64(note_hash, 'Not hash')}"


# NP-CONTRACT(02#5.1): imza sabit.
def registration_iri(note_hash: str) -> str:
    """Kayıt aktivitesinin (PROV-O) IRI'si: {NS}registration/{hash}."""
    return f"{NAMESPACE}registration/{_check_hex64(note_hash, 'Not hash')}"


# NP-CONTRACT(02#5.1): imza sabit. anchor/proof.py (Burak) proof dosyasının "@id" alanında aynı biçimi üretir.
def proof_iri(note_hash: str) -> str:
    """Proof'un IRI'si: {NS}proof/{hash}."""
    return f"{NAMESPACE}proof/{_check_hex64(note_hash, 'Not hash')}"


# NP-CONTRACT(02#5.1): imza sabit.
def account_iri(pseudonym: str) -> str:
    """Takma adlı hesabın IRI'si: {NS}account/{takma-ad}.

    Takma ad IRI içinde yüzde kodlamasıyla yazılır; böylece boşluk, "/" ya da "#" içeren bir takma ad
    IRI'yi bozmaz. Takma adda hangi karakterlere izin verildiği hesap açma (ARD-2) kuralıdır, burası değil.
    Gerçek isim ya da öğrenci numarası buraya gelmez (K-007).
    """
    if not isinstance(pseudonym, str) or not pseudonym.strip():
        raise ValueError("Takma ad boş olamaz.")
    return f"{NAMESPACE}account/{quote(pseudonym, safe='')}"


# NP-CONTRACT(02#5.1): imza sabit.
def timestamp_iri(txid: str) -> str:
    """Günlük timestamp'in IRI'si: {NS}timestamp/{txid}."""
    return f"{NAMESPACE}timestamp/{_check_hex64(txid, 'txid')}"


# NP-CONTRACT(02#5.1): imza sabit. Sözlükteki kimlikler Eylem'in ontology/courses.ttl dosyasından gelir.
def concept_iri(local_id: str) -> str:
    """Ders ya da konu yerel kimliğinden tam IRI: "Topic_FeeRate" -> {NS}Topic_FeeRate.

    Kimliğin sözlükte olup olmadığını denetlemez; o iş ontology.vocab.Vocabulary'nin (Eylem) ve
    SHACL'ın işidir. Burada yalnızca biçim denetlenir.
    """
    if not isinstance(local_id, str) or not _CONCEPT_ID.fullmatch(local_id):
        raise ValueError(f"Kimlik Course_<KOD> ya da Topic_<PascalCase> biçiminde olmalı: {local_id!r}")
    return f"{NAMESPACE}{local_id}"
