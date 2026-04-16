"""Central re-exports of all pre-computed introspection data.

This module aggregates version enums, weight mappings, and
compatibility maps for all supported operating systems, providing
a single entry point for the weight providers.
"""

from typing import Final

from tg_devices.enums.os import OS
from tg_devices.weight.introspection.android import (
    ANDROID_APP_WEIGHTS as ANDROID_APP_WEIGHTS,
)
from tg_devices.weight.introspection.android import (
    ANDROID_APPS as ANDROID_APPS,
)
from tg_devices.weight.introspection.android import (
    ANDROID_APPS_WEIGHTS as ANDROID_APPS_WEIGHTS,
)
from tg_devices.weight.introspection.android import (
    ANDROID_COMPATIBILITY_MAP as ANDROID_COMPATIBILITY_MAP,
)
from tg_devices.weight.introspection.android import (
    ANDROID_DEVICE_MODEL as ANDROID_DEVICE_MODEL,
)
from tg_devices.weight.introspection.android import (
    ANDROID_SYSTEM_WEIGHTS as ANDROID_SYSTEM_WEIGHTS,
)
from tg_devices.weight.introspection.android import (
    ANDROID_SYSTEMS as ANDROID_SYSTEMS,
)
from tg_devices.weight.introspection.android import (
    ANDROID_SYSTEMS_WEIGHTS as ANDROID_SYSTEMS_WEIGHTS,
)
from tg_devices.weight.introspection.android import (
    ANDROID_WEIGHTS_DT as ANDROID_WEIGHTS_DT,
)
from tg_devices.weight.introspection.linux import (
    LIN_APPS_WEIGHTS as LIN_APPS_WEIGHTS,
)
from tg_devices.weight.introspection.linux import (
    LIN_SYSTEMS_WEIGHTS as LIN_SYSTEMS_WEIGHTS,
)
from tg_devices.weight.introspection.linux import (
    LINUX_APP_WEIGHTS as LINUX_APP_WEIGHTS,
)
from tg_devices.weight.introspection.linux import (
    LINUX_APPS as LINUX_APPS,
)
from tg_devices.weight.introspection.linux import (
    LINUX_COMPATIBILITY_MAP as LINUX_COMPATIBILITY_MAP,
)
from tg_devices.weight.introspection.linux import (
    LINUX_DEVICE_MODEL as LINUX_DEVICE_MODEL,
)
from tg_devices.weight.introspection.linux import (
    LINUX_SYSTEM_WEIGHTS as LINUX_SYSTEM_WEIGHTS,
)
from tg_devices.weight.introspection.linux import (
    LINUX_SYSTEMS as LINUX_SYSTEMS,
)
from tg_devices.weight.introspection.linux import (
    LINUX_WEIGHTS_DT as LINUX_WEIGHTS_DT,
)
from tg_devices.weight.introspection.macos import (
    MAC_APPS as MAC_APPS,
)
from tg_devices.weight.introspection.macos import (
    MAC_APPS_WEIGHTS as MAC_APPS_WEIGHTS,
)
from tg_devices.weight.introspection.macos import (
    MAC_SYSTEMS as MAC_SYSTEMS,
)
from tg_devices.weight.introspection.macos import (
    MAC_SYSTEMS_WEIGHTS as MAC_SYSTEMS_WEIGHTS,
)
from tg_devices.weight.introspection.macos import (
    MACOS_APP_WEIGHTS as MACOS_APP_WEIGHTS,
)
from tg_devices.weight.introspection.macos import (
    MACOS_COMPATIBILITY_MAP as MACOS_COMPATIBILITY_MAP,
)
from tg_devices.weight.introspection.macos import (
    MACOS_DEVICE_MODEL as MACOS_DEVICE_MODEL,
)
from tg_devices.weight.introspection.macos import (
    MACOS_SYSTEM_WEIGHTS as MACOS_SYSTEM_WEIGHTS,
)
from tg_devices.weight.introspection.macos import (
    MACOS_WEIGHTS_DT as MACOS_WEIGHTS_DT,
)
from tg_devices.weight.introspection.windows import (
    WIN_APPS as WIN_APPS,
)
from tg_devices.weight.introspection.windows import (
    WIN_APPS_WEIGHTS as WIN_APPS_WEIGHTS,
)
from tg_devices.weight.introspection.windows import (
    WIN_SYSTEMS as WIN_SYSTEMS,
)
from tg_devices.weight.introspection.windows import (
    WIN_SYSTEMS_WEIGHTS as WIN_SYSTEMS_WEIGHTS,
)
from tg_devices.weight.introspection.windows import (
    WINDOWS_APP_WEIGHTS as WINDOWS_APP_WEIGHTS,
)
from tg_devices.weight.introspection.windows import (
    WINDOWS_COMPATIBILITY_MAP as WINDOWS_COMPATIBILITY_MAP,
)
from tg_devices.weight.introspection.windows import (
    WINDOWS_DEVICE_MODEL as WINDOWS_DEVICE_MODEL,
)
from tg_devices.weight.introspection.windows import (
    WINDOWS_SYSTEM_WEIGHTS as WINDOWS_SYSTEM_WEIGHTS,
)
from tg_devices.weight.introspection.windows import (
    WINDOWS_WEIGHTS_DT as WINDOWS_WEIGHTS_DT,
)

OS_NAMES: Final[tuple[OS, ...]] = tuple(OS)
