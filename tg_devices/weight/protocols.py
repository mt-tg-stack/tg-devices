"""Protocol definition for weight providers."""

from typing import Protocol

from tg_devices.compatibility.map import CompatibilityMap
from tg_devices.enums.app_version import AppVersion
from tg_devices.enums.device_model import DeviceModel
from tg_devices.enums.os import OS
from tg_devices.enums.system_version import SystemVersion


class IVersionWeight(Protocol):
    app_weights: tuple[int, ...]
    system_weights: tuple[int, ...]


class IOSProfile(Protocol):
    app_version: tuple[AppVersion, ...]
    system_version: tuple[SystemVersion, ...]
    device_model: tuple[DeviceModel, ...]
    selection_weight: int
    version_weights: IVersionWeight
    compatibility_map: CompatibilityMap


class IWeightProvider(Protocol):
    """Interface for providing OS selection weights and per-OS data."""

    def get_os_profile(self, os: OS) -> IOSProfile:
        """Return the profile bundle for a given OS.

        Args:
            os: The target operating system.

        Returns:
            A ``StaticOSWeights`` with versions, models, weights,
            and the pre-computed compatibility map.

        """
        ...

    def get_os_names(self) -> tuple[OS, ...]:
        """Return all supported operating systems.

        Returns:
            Tuple of ``OS`` enum members.

        """
        ...

    def get_os_probabilities(self) -> tuple[int, ...]:
        """Return all supported operating systems.

        Returns:
            Tuple of ``OS`` enum members.

        """
        ...
