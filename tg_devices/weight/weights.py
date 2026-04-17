"""Weight dataclasses for OS-level probability distributions."""

from dataclasses import dataclass

from tg_devices.compatibility.map import CompatibilityMap
from tg_devices.enums.app_version import AppVersion
from tg_devices.enums.device_model import DeviceModel
from tg_devices.enums.system_version import SystemVersion
from tg_devices.weight.protocols import (
    IOSProfile,
    IVersionWeight,
)


@dataclass
class VersionWeights(IVersionWeight):
    """Relative weights for app and system version selection.

    Weights are aligned positionally with the corresponding version
    enums and are passed directly to ``random.choices``.

    Attributes:
        app_weights: Weights aligned with available ``AppVersion`` enums.
        system_weights: Weights aligned with available ``SystemVersion`` enums.
    """

    app_weights: tuple[int, ...]
    system_weights: tuple[int, ...]


@dataclass
class OSProfile(IOSProfile):
    """Complete data bundle for generating a device profile on one OS.

    Encapsulates all static data the generator needs: known versions,
    device models, selection probability, version weights, and a
    pre-computed compatibility map.

    Attributes:
        app_versions: All known ``AppVersion`` values for this OS.
        system_versions: All known ``SystemVersion`` values for this OS.
        device_models: All known ``DeviceModel`` values for this OS.
        selection_weight: Relative probability (0–100) of picking this
            OS over others in the same pool.
        version_weights: Nested weights for internal version selection.
        compatibility_map: Maps each ``SystemVersion`` to the app
            versions valid for it and their corresponding weights.
    """

    app_version: tuple[AppVersion, ...]
    system_version: tuple[SystemVersion, ...]
    device_model: tuple[DeviceModel, ...]
    selection_weight: int
    version_weights: IVersionWeight
    compatibility_map: CompatibilityMap
