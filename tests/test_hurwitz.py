"""Hurwitz 24 + Hopf images match the checked-in fixtures."""

from __future__ import annotations

import json
from importlib.resources import files

import numpy as np

from flux_hopf_lib.hopf import hopf_map
from flux_hopf_lib.quaternion import HURWITZ_UNITS


def _load(name: str) -> dict:
    path = files("flux_hopf_lib.fixtures").joinpath(name)
    return json.loads(path.read_text(encoding="utf-8"))


def test_twenty_four_units_exact() -> None:
    data = _load("hurwitz_units_v1.json")
    want = np.asarray(data["units"], dtype=float)
    assert want.shape == (24, 4)
    np.testing.assert_array_equal(HURWITZ_UNITS, want)
    np.testing.assert_allclose(np.sum(HURWITZ_UNITS**2, axis=1), 1.0, atol=0)


def test_hopf_images_match_fixture() -> None:
    data = _load("hopf_hurwitz_v1.json")
    assert len(data["points"]) == 24
    for i, row in enumerate(data["points"]):
        q = np.asarray(row["q"], dtype=float)
        np.testing.assert_array_equal(q, HURWITZ_UNITS[i])
        y1, y2, y3 = hopf_map(*q)
        got = np.array([float(y1), float(y2), float(y3)])
        want = np.asarray(row["y"], dtype=float)
        np.testing.assert_allclose(got, want, rtol=0, atol=0)
        np.testing.assert_allclose(np.linalg.norm(got), 1.0, atol=1e-15)
