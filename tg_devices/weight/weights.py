"""Weight dataclasses for OS-level probability distributions."""

from dataclasses import dataclass

from tg_devices.enums.app_version import AppVersion
from tg_devices.enums.device_model import DeviceModel
from tg_devices.enums.system_version import SystemVersion


@dataclass
class Weights:
    """Probability weights for app and system version selection.

    These weights are used by the randomness provider to pick a
    version from the corresponding population tuple.

    Attributes:
        app_weights: Relative weights (integers) aligned with the
            available app version enums.
        system_weights: Relative weights (integers) aligned with the
            available system version enums.

    """

    app_weights: tuple[int, ...]
    system_weights: tuple[int, ...]


@dataclass
class StaticOSWeights:
    """Complete weight and data bundle for a single operating system.

    This dataclass encapsulates all the information needed by the
    generator to produce a profile for a specific OS, including
    historical and predicted version data.

    Attributes:
        app_version: All known app versions for this OS.
        system_version: All known system versions for this OS.
        device_model: All known device models for this OS.
        weight: Relative probability (0-100) of selecting this OS
            compared to others in the same budget.
        weights: Nested ``Weights`` for internal version selection.
        compatibility_map: Pre-computed mapping ensuring that the
            selected app version is valid for the chosen system version.

    """

    app_version: tuple[AppVersion, ...]
    system_version: tuple[SystemVersion, ...]
    device_model: tuple[DeviceModel, ...]
    weight: int
    weights: Weights
    compatibility_map: dict[
        SystemVersion, tuple[tuple[AppVersion, ...], tuple[int, ...]]
    ]
