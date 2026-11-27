# NOTEPROOF-FILE
# module:   tagger
# owner:    aleyna          second: eylem
# story:    S3
# contract: 02#5.3
# depends:  -
# status:   stable
"""FakeLLM: testlerde gerçek dil modelinin yerine geçen, ağa çıkmayan istemci (03 bölüm 8).

Önceden verilen yanıtları sırayla döndürür ve kendisine gönderilen istemleri saklar. Böylece testler
API anahtarı olmadan CI'da çalışır ve bozuk JSON gibi durumlar istenildiği an üretilebilir.
"""

from __future__ import annotations


class FakeLLM:
    def __init__(self, *responses: str) -> None:
        if not responses:
            raise ValueError("FakeLLM en az bir yanıtla kurulmalı.")
        self._responses = list(responses)
        self.calls: list[tuple[str, str | None]] = []  # (prompt, system)

    def complete(self, prompt: str, *, system: str | None = None) -> str:
        self.calls.append((prompt, system))
        # Yanıtlar bitince son yanıt tekrarlanır.
        return self._responses[min(len(self.calls), len(self._responses)) - 1]
