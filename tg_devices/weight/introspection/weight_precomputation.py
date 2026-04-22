"""
Module for computing weights for enum members based on a Gaussian curve.
"""

import math
from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum
from typing import Final, TypeVar

from tg_devices.compatibility.inspection import parse_version
from tg_devices.enums.os import OS

E = TypeVar("E", bound=StrEnum)


@dataclass(frozen=True)
class WeightCurveParams:
    """Parameters controlling the weight distribution shape.

    Args:
        peak_ratio:   Where the peak sits as a fraction of the enum range.
                      0.0 = first member, 1.0 = last member.
                      Typical: 0.55–0.65 for app versions (users lag behind
                      the latest release), 0.70–0.80 for system versions.
        sigma_left:   Spread of the *left* (older) side, as a fraction of
                      total enum length.  Larger → softer rise.
        sigma_right:  Spread of the *right* (newer) side.
                      Smaller → steeper drop-off for cutting-edge versions.
        max_weight:   Weight assigned at the peak.
        min_weight:   Floor — every member gets at least this value.
    """

    peak_ratio: float = 0.65
    sigma_left: float = 0.28
    sigma_right: float = 0.20
    max_weight: int = 30
    min_weight: int = 1

    def __post_init__(self) -> None:
        if not 0.0 < self.peak_ratio < 1.0:
            raise ValueError("peak_ratio must be in (0, 1)")
        if self.sigma_left <= 0 or self.sigma_right <= 0:
            raise ValueError("sigma values must be positive")
        if self.max_weight < self.min_weight:
            raise ValueError("max_weight must be >= min_weight")


PLATFORM_DEFAULTS: Final[dict[OS, dict[str, WeightCurveParams]]] = {
    OS.ANDROID: {
        "app": WeightCurveParams(
            peak_ratio=0.55, sigma_left=0.25, sigma_right=0.22, max_weight=30
        ),
        "sys": WeightCurveParams(
            peak_ratio=0.78, sigma_left=0.30, sigma_right=0.16, max_weight=25
        ),
    },
    OS.LINUX: {
        "app": WeightCurveParams(
            peak_ratio=0.65, sigma_left=0.28, sigma_right=0.20, max_weight=30
        ),
        "sys": WeightCurveParams(
            peak_ratio=0.70, sigma_left=0.30, sigma_right=0.20, max_weight=25
        ),
    },
    OS.WINDOWS: {
        "app": WeightCurveParams(
            peak_ratio=0.60, sigma_left=0.25, sigma_right=0.25, max_weight=30
        ),
        "sys": WeightCurveParams(
            peak_ratio=0.75, sigma_left=0.30, sigma_right=0.20, max_weight=25
        ),
    },
    OS.MACOS: {
        "app": WeightCurveParams(
            peak_ratio=0.60, sigma_left=0.25, sigma_right=0.25, max_weight=30
        ),
        "sys": WeightCurveParams(
            peak_ratio=0.75, sigma_left=0.30, sigma_right=0.20, max_weight=25
        ),
    },
}


def compute_weights(  # noqa: UP047
    enum_class: type[E],
    params: WeightCurveParams | None = None,
    *,
    peak_ratio: float | None = None,
    sigma_left: float | None = None,
    sigma_right: float | None = None,
    max_weight: int | None = None,
    min_weight: int | None = None,
) -> Mapping[E, int]:
    """
    Compute weights for enum members based on a Gaussian curve.

    Args:
        enum_class: The enum class whose members to weight.
        params: Optional base parameters for the weight curve. If not provided,
                defaults from PLATFORM_DEFAULTS will be used based on context.
        peak_ratio: Overrides the default peak_ratio in params.
        sigma_left: Overrides the default sigma_left in params.
        sigma_right: Overrides the default sigma_right in params.
        max_weight: Overrides the default max_weight in params.
        min_weight: Overrides the default min_weight in params.
    Returns:
        A mapping from enum members to their computed weights.
    """
    base = params or WeightCurveParams()
    effective = WeightCurveParams(
        peak_ratio=peak_ratio if peak_ratio is not None else base.peak_ratio,
        sigma_left=sigma_left if sigma_left is not None else base.sigma_left,
        sigma_right=sigma_right
        if sigma_right is not None
        else base.sigma_right,
        max_weight=max_weight if max_weight is not None else base.max_weight,
        min_weight=min_weight if min_weight is not None else base.min_weight,
    )

    members = sorted(enum_class, key=lambda m: parse_version(m.value))
    n = len(members)

    if n == 0:
        return {}
    if n == 1:
        return {members[0]: effective.max_weight}

    peak_pos = effective.peak_ratio * (n - 1)

    raw: list[float] = []
    for i in range(n):
        d = i - peak_pos
        sigma = (effective.sigma_left if d <= 0 else effective.sigma_right) * (
            n - 1
        )
        raw.append(math.exp(-0.5 * (d / sigma) ** 2))

    hi = max(raw)
    result: dict[E, int] = {}
    for member, score in zip(members, raw):
        w = effective.min_weight + (
            (effective.max_weight - effective.min_weight) * (score / hi)
        )
        result[member] = max(effective.min_weight, round(w))

    return result
