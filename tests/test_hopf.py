"""Hopf fibration tests."""

from __future__ import annotations

import numpy as np

from flux_hopf_lib.hopf import hopf_coordinates, hopf_map, hopf_map_from_angles
from flux_hopf_lib.hopf.hopfion import toroidal_hopfion_director
from flux_hopf_lib.utils import cartesian_grid


def test_hopf_coordinates_on_s3():
    eta = np.array(0.7)
    xi1 = np.array(0.3)
    xi2 = np.array(1.1)
    x1, x2, x3, x4 = hopf_coordinates(eta, xi1, xi2)
    n2 = x1**2 + x2**2 + x3**2 + x4**2
    assert abs(float(n2) - 1.0) < 1e-10


def test_hopf_map_on_s2():
    y1, y2, y3 = hopf_map_from_angles(np.array(0.4), np.array(0.2), np.array(0.9))
    n = np.sqrt(y1**2 + y2**2 + y3**2)
    assert abs(float(n) - 1.0) < 1e-9


def test_hopf_map_vectorized():
    eta = np.linspace(0.1, 1.0, 5)
    xi1 = np.linspace(0.0, 2.0, 5)
    xi2 = np.linspace(0.0, 1.5, 5)
    y1, y2, y3 = hopf_map(*hopf_coordinates(eta, xi1, xi2))
    norms = np.sqrt(y1**2 + y2**2 + y3**2)
    assert np.allclose(norms, 1.0, atol=1e-8)


def test_hopf_map_is_classical_not_legacy():
    y1, y2, y3 = hopf_map(
        np.array(0.0), np.array(0.0), np.array(1.0), np.array(0.0)
    )
    assert abs(float(y1)) < 1e-12
    assert abs(float(y2)) < 1e-12
    assert abs(float(y3) + 1.0) < 1e-12


def test_hopf_map_fiber_constancy_under_common_phase():
    rng = np.random.default_rng(3)
    q = rng.normal(size=4)
    q = q / np.linalg.norm(q)
    y0 = np.array(hopf_map(*q))
    for phi in np.linspace(0.0, 2.0 * np.pi, 16, endpoint=False):
        c, s = np.cos(phi), np.sin(phi)
        # left multiply by e^{iφ} = (c, s, 0, 0)
        w, x, y, z = q
        qp = np.array(
            [
                c * w - s * x,
                c * x + s * w,
                c * y - s * z,
                c * z + s * y,
            ]
        )
        y = np.array(hopf_map(*qp))
        assert np.allclose(y, y0, atol=1e-10)


def test_legacy_portal_map_is_not_hopf_map():
    from flux_hopf_lib.hopf.fibration import legacy_portal_map

    q = np.array([0.0, 0.0, 1.0, 0.0])
    y_h = np.array(hopf_map(*q))
    y_l = np.array(legacy_portal_map(*q))
    assert not np.allclose(y_h, y_l, atol=1e-6)


def test_unit_input_not_output_normalized():
    x1, x2, x3, x4 = 0.5, 0.5, 0.5, 0.5
    n = (x1**2 + x2**2 + x3**2 + x4**2) ** 0.5
    x1, x2, x3, x4 = x1 / n, x2 / n, x3 / n, x4 / n
    y = np.array(hopf_map(x1, x2, x3, x4), dtype=float)
    raw = np.array(
        [
            2.0 * (x1 * x3 + x2 * x4),
            2.0 * (x1 * x4 - x2 * x3),
            x1**2 + x2**2 - x3**2 - x4**2,
        ]
    )
    assert np.allclose(y, raw, atol=1e-12)


def test_hopfion_unit():
    x, y = cartesian_grid(16, 16, extent=2.0)
    z = np.zeros_like(x)
    nx, ny, nz = toroidal_hopfion_director(x, y, z)
    norms = np.sqrt(nx**2 + ny**2 + nz**2)
    assert np.allclose(norms, 1.0, atol=1e-8)
