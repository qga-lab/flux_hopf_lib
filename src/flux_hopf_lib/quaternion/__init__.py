"""Quaternion algebra and rotors (numpy core; optional torch)."""

from flux_hopf_lib.quaternion.core import (
    Quaternion,
    decode_shard,
    encode_shard,
    q_conj,
    q_mult,
    q_normalize,
    rodrigues_rotation,
    small_rotor,
)
from flux_hopf_lib.quaternion.hurwitz import HURWITZ_UNITS

__all__ = [
    "HURWITZ_UNITS",
    "Quaternion",
    "q_mult",
    "q_conj",
    "q_normalize",
    "small_rotor",
    "rodrigues_rotation",
    "encode_shard",
    "decode_shard",
]
