"""Public API for the tg-devices library.

This module provides the core functionality for generating realistic,
statistically plausible, and technically compatible device profiles
for Telegram clients.

Typical usage example:

    from tg_devices import DeviceProfileGenerator, OS

    # Initialize the generator with default weights
    gen = DeviceProfileGenerator()

    # Generate a random profile
    profile = gen.generate_os_profile()

    # Generate a profile for a specific OS with custom overrides
    gen_custom = DeviceProfileGenerator(windows=40, android=60)
    android_profile = gen_custom.generate_os_profile(os=OS.ANDROID)
"""

from tg_devices.enums.os import OS
from tg_devices.generator.generator import DeviceProfileGenerator
from tg_devices.generator.profile import OSProfile

__all__ = ["OS", "DeviceProfileGenerator", "OSProfile"]
