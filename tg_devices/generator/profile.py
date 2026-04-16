"""Dataclass representing a generated device profile."""

from dataclasses import dataclass


@dataclass(frozen=True)
class OSProfile:
    """Immutable device profile for a Telegram client session.

    This dataclass contains the final, string-serialized output of
    the generation process, representing a realistic configuration
    that can be used by a Telegram client.

    Attributes:
        os: The human-readable name of the operating system.
        app_version: The version string for the Telegram application.
        system_version: The version string for the underlying OS.
        device_model: The hardware model or identifier for the device.

    """

    os: str
    app_version: str
    system_version: str
    device_model: str
