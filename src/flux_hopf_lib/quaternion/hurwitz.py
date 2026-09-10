"""The 24 Hurwitz units. Source of truth for QGA and VQC consumers.

Coordinates: ``q = (x1, x2, x3, x4) = (w, x, y, z)``.
Order: ±1, ±i, ±j, ±k (minus then plus on each axis), then
``(±1 ± i ± j ± k)/2`` via ``itertools.product([-1/2, 1/2], repeat=4)``
with the last index fastest.

These are the integer Hurwitz units of norm 1. Cardinality 24 is a theorem.
The listed order is a Software fact of this package.
"""

from __future__ import annotations

from itertools import product

import numpy as np
from numpy.typing import NDArray

Array = NDArray[np.floating]


def _hurwitz_units() -> Array:
    units: list[list[float]] = []
    for i in range(4):
        for sgn in (-1.0, 1.0):
            v = [0.0, 0.0, 0.0, 0.0]
            v[i] = sgn
            units.append(v)
    for signs in product([-0.5, 0.5], repeat=4):
        units.append(list(signs))
    arr = np.asarray(units, dtype=float)
    if arr.shape != (24, 4):
        raise RuntimeError(f"Hurwitz units must be 24×4, got {arr.shape}")
    return arr


HURWITZ_UNITS: Array = _hurwitz_units()
