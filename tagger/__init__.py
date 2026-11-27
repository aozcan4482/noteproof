# NOTEPROOF-FILE
# module:   tagger
# owner:    aleyna          second: eylem
# story:    S3
# contract: 02#5.3
# depends:  -
# status:   wip
"""AI tagger: notun metninden ders, konu ve iki cümlelik özet önerir (aktivite modeli, adım 4a).

Üç kesin sınır (uyeler/aleyna.md, 02#5.3):
1. Yalnızca önerir; hiçbir şey kaydetmez. Kaydı, yazar onayladıktan sonra kayıt servisi (Arda) yapar.
2. Yalnızca sözlükten seçer; modelin yanıtı kodla süzülür.
3. Dil modelini etiketleme için çağıran tek bileşendir; başka modüller modele tagger/llm.py üzerinden ulaşır.

Diğer modüller bu paketten yalnızca 02#5.3'teki adları içe aktarır:
    tagger.llm.LLMClient, tagger.llm.client_from_env
    tagger.suggest.TagSuggestion, tagger.suggest.suggest
"""
