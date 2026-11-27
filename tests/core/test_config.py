# NOTEPROOF-FILE
# module:   core
# owner:    arda            second: burak
# story:    -
# contract: 02#5.1, 02#8
# depends:  core.config.data_dir
# status:   stable
"""core/config.py testleri: NOTEPROOF_DATA_DIR ve varsayılan ./data."""

from __future__ import annotations

import pathlib

import pytest

from core.config import data_dir


def test_default_is_data_in_working_directory(monkeypatch):
    monkeypatch.delenv("NOTEPROOF_DATA_DIR", raising=False)
    assert data_dir() == pathlib.Path("./data")


def test_env_variable_wins(monkeypatch, tmp_path):
    monkeypatch.setenv("NOTEPROOF_DATA_DIR", str(tmp_path))
    assert data_dir() == tmp_path


def test_does_not_create_the_folder(monkeypatch, tmp_path):
    target = tmp_path / "yok"
    monkeypatch.setenv("NOTEPROOF_DATA_DIR", str(target))
    data_dir()
    assert not target.exists()


@pytest.mark.parametrize("empty", ["", "   "])
def test_empty_env_variable_is_an_error(monkeypatch, empty):
    monkeypatch.setenv("NOTEPROOF_DATA_DIR", empty)
    with pytest.raises(ValueError):
        data_dir()
