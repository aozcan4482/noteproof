"""opreturn.py testleri: zincire yalnızca 32 byte'lık kök gidebilir."""

import pytest

from anchor import opreturn

ROOT = bytes(range(32))


def test_script_layout():
    script = opreturn.build_script(ROOT)
    assert script.hex() == "6a20" + ROOT.hex()
    assert len(script) == 34


@pytest.mark.parametrize("size", [0, 31, 33, 80])
def test_only_32_bytes_allowed(size):
    with pytest.raises(ValueError):
        opreturn.build_script(bytes(size))


def test_parse_round_trip():
    assert opreturn.parse_root(opreturn.build_script(ROOT).hex()) == ROOT


@pytest.mark.parametrize(
    "script_hex",
    [
        "6a21" + "00" * 33,            # 33 byte
        "6a" + "4c20" + "00" * 32,     # farklı push biçimi
        "6a20" + "00" * 31,            # eksik
        "0014" + "00" * 20,            # normal adres çıktısı
        "zz",
    ],
)
def test_parse_rejects_other_scripts(script_hex):
    assert opreturn.parse_root(script_hex) is None


def tx(*scripts):
    return {"vout": [{"scriptPubKey": {"hex": s}} for s in scripts]}


def test_tx_holds_only_root():
    change = "0014" + "11" * 20
    good = opreturn.build_script(ROOT).hex()
    assert opreturn.tx_holds_only_root(tx(good, change))
    assert not opreturn.tx_holds_only_root(tx(change))
    assert not opreturn.tx_holds_only_root(tx(good, good))
    assert not opreturn.tx_holds_only_root(tx("6a0568656c6c6f", change))  # "hello"
