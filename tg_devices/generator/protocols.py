"""Protocol definition for device profile generators."""

from typing import Protocol

from tg_devices.enums.os import OS
from tg_devices.generator.profile import OSProfile


class IDeviceProfileGenerator(Protocol):
    """Interface for device profile generators."""

    def generate_os_profile(self, os: OS | None = None) -> OSProfile:
        """Generate a device profile, optionally for a specific OS.

        Args:
            os: Target operating system. If ``None``, an OS is
                chosen via weighted random selection.

        Returns:
            A frozen ``OSProfile`` with compatible version fields.

        """
        ...
