# NOTEPROOF-FILE
# module:   evalset
# owner:    emine           second: aleyna
# story:    S3, S6
# contract: -
# depends:  -
# status:   stable
"""Değerlendirme seti (evalset/): AI tagger ve kopya uyarısını ölçen 60 not + 20 planted copy.

  notes/          -> ekibin KENDİ notları, düz metin (<id>.txt)
  manifest.csv    -> her notun bilinen dersi, konuları, takma adlı yazarı ve kayıt zamanı
  planted/        -> plant.py'nin ürettiği 20 kopya (<copy_id>.txt) ve planted.csv
  plant.py        -> kopyaları sabit bir seed ile üretir (tekrar üretilebilir)
  run_copywarn.py -> kopya uyarısını ölçer; hedefin altındaysa CI'yı kırar

Ayrıntılar: evalset/README.md
"""
