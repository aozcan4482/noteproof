# NOTEPROOF-FILE
# module:   core
# owner:    arda            second: burak
# story:    -
# contract: 02#5.1
# depends:  core.graph.open_store
# status:   stable
"""core/graph.py testleri: depo açılır, yazılan üçlü kalıcıdır, varsayılan yer data_dir()/graph."""

from __future__ import annotations

import gc

import pytest

pyoxigraph = pytest.importorskip("pyoxigraph")

from core.graph import open_store  # noqa: E402
from core.ns import note_iri  # noqa: E402

HASH = "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
STATUS = "https://github.com/aozcan4482/noteproof/ns#status"


def _quad() -> "pyoxigraph.Quad":
    return pyoxigraph.Quad(
        pyoxigraph.NamedNode(note_iri(HASH)),
        pyoxigraph.NamedNode(STATUS),
        pyoxigraph.Literal("registered"),
    )


def test_open_store_creates_folder_and_persists(tmp_path):
    folder = tmp_path / "graph"
    store = open_store(folder)
    assert folder.is_dir()
    store.add(_quad())
    store.flush()
    del store
    gc.collect()  # Oxigraph kilidi nesne kapanınca bırakır

    reopened = open_store(folder)
    assert list(reopened.quads_for_pattern(None, None, None)) == [_quad()]


def test_default_location_is_data_dir_graph(monkeypatch, tmp_path):
    monkeypatch.setenv("NOTEPROOF_DATA_DIR", str(tmp_path))
    store = open_store()
    assert isinstance(store, pyoxigraph.Store)
    assert (tmp_path / "graph").is_dir()
