"""Protocol definition for weight providers."""

from typing import Protocol

from tg_devices.enums.os import OS
from tg_devices.weight.weights import StaticOSWeights


class IWeightProvider(Protocol):
    """Interface for providing OS selection weights and per-OS data."""

    def get_os_weights(self, os: OS) -> StaticOSWeights:
        """Return the complete weight bundle for a given OS.

        Args:
            os: The target operating system.

        Returns:
            A ``StaticOSWeights`` instance containing versions,
            models, weights, and the compatibility map.

        """
        ...

    def get_os_names(self) -> tuple[OS, ...]:
        """Return all supported operating systems.

        Returns:
            Tuple of ``OS`` enum members.

        """
        ...

    def get_os_probabilities(self) -> tuple[int, ...]:
        """Return selection probabilities for each OS.

        Returns:
            Tuple of integer weights aligned with ``get_os_names()``.

        """
        ...
