"""Protocol definition for device profile generators."""

from typing import Protocol

from tg_devices.enums.os import OS
from tg_devices.generator.profile import DeviceProfile
from tg_devices.weight.protocols import IOSProfile


class IDeviceProfileGenerator(Protocol):
    """Interface for device profile generators."""

    def generate_device_profile(
        self,
        os: OS | None = None,
        os_profile: IOSProfile | None = None,
    ) -> DeviceProfile:
        """Generate a complete device profile.

        Selects an OS (or uses the one provided), then picks a
        system version, a compatible app version, and a device model
        using weighted random selection.

        Args:
            os: Target operating system. If ``None``, an OS is
                chosen via weighted random selection.
            os_profile: Optional pre-fetched OS profile to use for generation.
                If not provided, it will be retrieved from the weight
                provider based on the chosen OS.

        Returns:
            A frozen ``OSProfile`` with all fields populated.

        """
        ...
