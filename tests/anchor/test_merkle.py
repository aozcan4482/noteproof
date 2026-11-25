"""merkle.py testleri: kök, path ve doğrulama."""

import hashlib

import pytest

from anchor import merkle


def note_hashes(n: int) -> list[bytes]:
    # Gerçek notların yerine "not-0", "not-1", ... metinlerinin SHA-256'sı.
    return [hashlib.sha256(f"not-{i}".encode()).digest() for i in range(n)]


@pytest.mark.parametrize("n", [1, 2, 3, 4, 5, 7, 8, 40, 101])
def test_every_path_verifies(n):
    hashes = note_hashes(n)
    root, paths = merkle.build_tree(hashes)
    assert len(root) == 32
    for h, path in zip(hashes, paths):
        assert merkle.verify_path(h, path, root)


def test_single_note_root_is_its_leaf():
    (h,) = note_hashes(1)
    assert merkle.merkle_root([h]) == merkle.hash_leaf(h)
    assert merkle.merkle_path([h], 0) == []


def test_known_two_leaf_root():
    a, b = note_hashes(2)
    expected = merkle.sha256(b"\x01" + merkle.sha256(b"\x00" + a) + merkle.sha256(b"\x00" + b))
    assert merkle.merkle_root([a, b]) == expected


def test_odd_node_is_promoted_not_duplicated():
    a, b, c = note_hashes(3)
    expected = merkle.hash_node(merkle.hash_node(merkle.hash_leaf(a), merkle.hash_leaf(b)), merkle.hash_leaf(c))
    assert merkle.merkle_root([a, b, c]) == expected
    # Bitcoin tarzı kopyalama yapsaydık [a,b,c] ile [a,b,c,c] aynı kökü verirdi.
    assert merkle.merkle_root([a, b, c]) != merkle.merkle_root([a, b, c, c])


def test_wrong_note_fails():
    hashes = note_hashes(8)
    root, paths = merkle.build_tree(hashes)
    assert not merkle.verify_path(hashes[1], paths[0], root)


def test_tampered_path_fails():
    hashes = note_hashes(8)
    root, paths = merkle.build_tree(hashes)
    step = paths[3][0]
    bad = [merkle.PathStep(step.side, bytes(32))] + paths[3][1:]
    assert not merkle.verify_path(hashes[3], bad, root)


def test_wrong_root_fails():
    hashes = note_hashes(4)
    _, paths = merkle.build_tree(hashes)
    assert not merkle.verify_path(hashes[0], paths[0], bytes(32))


def test_internal_node_cannot_pose_as_leaf():
    # İki yaprağın birleşimini "not hash'i" gibi vermek kanıt üretmemeli.
    a, b = note_hashes(2)
    fake_note = merkle.hash_node(merkle.hash_leaf(a), merkle.hash_leaf(b))
    root = merkle.merkle_root([a, b])
    assert not merkle.verify_path(fake_note, [], root)


def test_rejects_empty_and_bad_sizes():
    with pytest.raises(ValueError):
        merkle.build_tree([])
    with pytest.raises(ValueError):
        merkle.build_tree([b"kisa"])
