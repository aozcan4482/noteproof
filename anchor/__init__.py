# NOTEPROOF-FILE
# module:   anchor
# owner:    burak           second: arda
# story:    S1, S2, S7
# contract: -
# depends:  -
# status:   stable
"""NoteProof — Bitcoin timestamp servisi (anchor/).

Bu paket proposal'daki "Bitcoin timestamp service" modülüdür:
  1. Kayıt servisi her notun SHA-256 hash'ini kuyruğa ekler  -> store.py
  2. Günde bir kez kuyruktaki hash'lerden Merkle tree kurulur -> merkle.py
  3. Ağacın 32 byte'lık kökü OP_RETURN çıktısıyla signet'e yazılır -> opreturn.py, rpc.py
  4. İşlem onaylanınca her not için bir proof dosyası üretilir -> proof.py
  5. Bütün akışı daily.py yönetir (cron ile her gün 23:00'te çalışır).
"""
