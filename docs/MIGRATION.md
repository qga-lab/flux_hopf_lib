# Migrating consumers to flux_hopf_lib

## Hopf map (0.3.0)

`hopf.fibration.hopf_map` is the classical real map (QGA Chapter 2). Numerical
output **changed** relative to ≤0.2.6. The old three-component formula is
`legacy_portal_map` and is not a Hopf map.

```python
from flux_hopf_lib.hopf import hopf_map, hopf_map_classical, legacy_portal_map

# h(0,0,1,0) == (0, 0, -1); constant on common-phase fibers
```

Pin `flux-hopf-lib==0.2.6` only if you need the old numbers; prefer calling
`legacy_portal_map` by name. `kingdom.core.hopf` re-exports this module.

## Status (2026-07)

| Consumer | Migration |
|----------|-----------|
| mystery | **done** |
| toe | **done** (shim + mixins; full RubikCone stays local) |
| vqc_proto | **done** |
| vqc_sims_public | **done** |
| hfb | **done** |
| kingdom | **done** |
| vqc_workbench | **done** (required `flux-hopf-lib>=0.3.0`; `core/geometry.py` re-exports Quaternion / encode_shard; `hopf_map` calls `hopf_map_quaternion`) |

Ongoing: more PDE helpers / invariants move into core as they prove shared.

---

## vqc_workbench

Dropped the local `Quaternion` and the forked `hopf_map` (component/sign variant plus `‖y‖` renormalize). Install the core, then keep only a call-shape wrapper:

```bash
pip install -e ../flux_hopf_lib
# or: flux-hopf-lib>=0.3.0
```

```python
from flux_hopf_lib.quaternion import Quaternion, encode_shard
from flux_hopf_lib.hopf import hopf_map_quaternion
```

## Principle

1. Install `flux-hopf-lib` (editable during development; pin `@v0.1.0` for HF).
2. Replace `sys.path` / `importlib` loads of sibling repo files with package imports.
3. Keep specialized classes in their repos; only shared primitives move here.
4. Optionally leave thin re-exports in the old modules for one release cycle.
5. **Depend on the core, not on sibling repos**, for quaternion / Hopf / survival math.

---

## mystery (first)

### Before (fragile)

```python
import sys
from pathlib import Path
TOE_SRC = Path.home() / "Projects" / "toe" / "src"
sys.path.insert(0, str(TOE_SRC))
# or importlib.util.spec_from_file_location("relaxation_survival", ...)
```

### After

```python
# requirements.txt
# -e ../flux_hopf_lib
# numpy>=1.24
# scipy>=1.10
# matplotlib>=3.7

from flux_hopf_lib import PHI, E, PI, R_RESIDUAL, E_INV2, DEFAULT_KAPPA
from flux_hopf_lib.simulation import (
    simulate_twist_pde_survival,
    evolve_gauged_twist_survival,
    compare_to_analogs,
    steps_for_lambda_t,
    LambdaTNormalization,
    SurvivalAnalogs,
)
from flux_hopf_lib.conduit import apply_golden_angle_increment
```

### Scripts to update (high priority)

| Script | Old source | New import |
|--------|------------|------------|
| `exponential_survival_probe.py` | toe `relaxation_survival` | `flux_hopf_lib.simulation` |
| `kappa_survival_sweep.py` | toe `relaxation_survival` | `flux_hopf_lib.simulation` + `kappa` |
| `pde_survival_eigenstructure.py` | hard-coded `~/Projects/toe/...` | `flux_hopf_lib.simulation` |
| `analog_comparative_sweep.py` | importlib toe | same |
| `meta_optimize_phi_probe.py` | toe src path | survival from lib; `RubikConeConduit` still from toe |

**Note:** Full `RubikConeConduit` remains in toe until a later phase. Mystery scripts
that need the torch conduit still depend on toe, but survival/κ/PDE no longer do.

```bash
# mystery development env
cd ~/Projects/mystery
pip install -e ../flux_hopf_lib
# optional for conduit probes:
pip install -e ../toe   # or keep toe venv + path for torch only
```

### space/mystery/demo_core.py

Replace the block that loads:

```python
toe_rs = Path.home() / "Projects" / "toe" / "src" / "relaxation_survival.py"
```

with:

```python
from flux_hopf_lib.simulation import simulate_twist_pde_survival, compare_to_analogs
```

For HF Spaces, either vendor a wheel or add to `requirements.txt`:

```text
# once published:
# flux-hopf-lib==0.1.0
# or git+https://github.com/qga-lab/flux_hopf_lib.git@v0.1.0
```

---

## toe (second)

1. Add dependency: `flux-hopf-lib` (editable).
2. In `src/relaxation_survival.py`, re-export from the core package:

```python
"""Deprecated local copy — prefer flux_hopf_lib.simulation."""
from flux_hopf_lib.simulation.survival import *  # noqa: F403
from flux_hopf_lib.constants import PHI, E, PI, R_RESIDUAL, E_INV2  # noqa: F401
```

3. In `conduit.py`, import shared helpers:

```python
from flux_hopf_lib.conduit import apply_golden_angle_increment, GoldenAngleMixin
from flux_hopf_lib.constants import GOLDEN_ANGLE_DEG, GOLDEN_ANGLE_RAD, PHI_INV2, W_G_LOCK
from flux_hopf_lib.quaternion.torch_ops import qmul, qnormalize  # optional
```

4. Keep `RubikConeConduit` / training stack local.

---

## vqc_proto (third) — done

`proto/orbital_braille/quaternion_codec.py` (and HF Space mirror) re-exports:

```python
from flux_hopf_lib.quaternion import Quaternion, encode_shard, decode_shard, rodrigues_rotation
```

Keep LG modes, typehead, QEC, and OAM imprint scales in vqc_proto — they are
application-specific.

---

## hfb (fourth) — done

```python
from flux_hopf_lib.hopf import hopf_map, hopf_coordinates, toroidal_hopfion_director
from flux_hopf_lib.flux import gaussian_defect, toroidal_bubble_wall
from flux_hopf_lib.utils import cartesian_grid, laplacian_fft
```

`hfb.hopf`, `hfb.utils.grid`, and shared `hfb.defects.densities` re-export the
core; hemi-void / `build_defect_density` stay HFB-local.

---

## kingdom (last) — done

Portal (`kingdom_come`) re-exports:

```python
from kingdom.core.constants import PHI, R_RESIDUAL, DEFAULT_KAPPA, W_G_LOCK
from kingdom.core import hopf_map, Quaternion  # → flux_hopf_lib under the hood
```

Investigation 6 and theory pages format live constants from the core package.

---

## Compatibility checklist

- [ ] `pytest` green in `flux_hopf_lib`
- [ ] mystery scripts that only need survival/κ run without toe on `PYTHONPATH`
- [ ] conduit-dependent mystery scripts still find toe (or `pip install -e ../toe`)
- [ ] hfb / vqc_proto tests unchanged after re-exports
- [ ] Version pin recorded in each consumer `requirements.txt` / `pyproject.toml`
