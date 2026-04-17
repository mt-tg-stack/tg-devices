"""Pre-computed static weight data for Windows."""

from collections.abc import Mapping
from typing import Final

from tg_devices.compatibility.map import get_compatibility_map
from tg_devices.enums.app_version import AppVersion
from tg_devices.enums.os import OS
from tg_devices.enums.system_version import SystemVersion
from tg_devices.enums.windows import (
    WindowsAppVersion,
    WindowsDesktopModel,
    WindowsSystemVersion,
)
from tg_devices.weight.weights import VersionWeights

WINDOWS_APP_WEIGHTS: Final[Mapping[WindowsAppVersion, int]] = {
    WindowsAppVersion.V4_8_3_X64: 1,
    WindowsAppVersion.V4_8_3_X86: 1,
    WindowsAppVersion.V4_8_1_X64: 1,
    WindowsAppVersion.V4_9_9_X64: 1,
    WindowsAppVersion.V4_9_9_X86: 1,
    WindowsAppVersion.V4_9_6_X64: 1,
    WindowsAppVersion.V4_9_4_X64: 1,
    WindowsAppVersion.V4_10_4_X64: 1,
    WindowsAppVersion.V4_10_3_X64: 1,
    WindowsAppVersion.V4_10_2_X64: 1,
    WindowsAppVersion.V4_11_6_X64: 1,
    WindowsAppVersion.V4_11_5_X64: 1,
    WindowsAppVersion.V4_11_3_X64: 1,
    WindowsAppVersion.V4_11_2_X64: 1,
    WindowsAppVersion.V4_12_2_X64: 1,
    WindowsAppVersion.V4_12_0_X64: 1,
    WindowsAppVersion.V4_13_1_X64: 1,
    WindowsAppVersion.V4_13_0_X64: 1,
    WindowsAppVersion.V4_14_9_X64: 2,
    WindowsAppVersion.V4_14_4_X64: 1,
    WindowsAppVersion.V4_14_1_X64: 1,
    WindowsAppVersion.V4_15_4_X64: 2,
    WindowsAppVersion.V4_15_2_X64: 1,
    WindowsAppVersion.V4_15_0_X64: 1,
    WindowsAppVersion.V4_16_9_X64: 3,
    WindowsAppVersion.V4_16_8_X64: 2,
    WindowsAppVersion.V4_16_7_X64: 2,
    WindowsAppVersion.V4_16_6_X64: 1,
    WindowsAppVersion.V5_0_4_X64: 3,
    WindowsAppVersion.V5_0_2_X64: 2,
    WindowsAppVersion.V5_0_1_X64: 2,
    WindowsAppVersion.V5_1_9_X64: 3,
    WindowsAppVersion.V5_1_7_X64: 2,
    WindowsAppVersion.V5_1_4_X64: 2,
    WindowsAppVersion.V5_2_3_X64: 3,
    WindowsAppVersion.V5_2_1_X64: 2,
    WindowsAppVersion.V5_3_3_X64: 3,
    WindowsAppVersion.V5_3_2_X64: 2,
    WindowsAppVersion.V5_3_1_X64: 2,
    WindowsAppVersion.V5_4_1_X64: 3,
    WindowsAppVersion.V5_5_5_X64: 5,
    WindowsAppVersion.V5_5_4_X64: 4,
    WindowsAppVersion.V5_5_3_X64: 3,
    WindowsAppVersion.V5_5_2_X64: 3,
    WindowsAppVersion.V5_5_1_X64: 2,
    WindowsAppVersion.V5_5_0_X64: 2,
    WindowsAppVersion.V5_6_3_X64: 5,
    WindowsAppVersion.V5_6_2_X64: 4,
    WindowsAppVersion.V5_6_1_X64: 3,
    WindowsAppVersion.V5_6_0_X64: 2,
    WindowsAppVersion.V5_7_2_X64: 5,
    WindowsAppVersion.V5_7_1_X64: 4,
    WindowsAppVersion.V5_7_0_X64: 3,
    WindowsAppVersion.V5_8_3_X64: 5,
    WindowsAppVersion.V5_8_2_X64: 4,
    WindowsAppVersion.V5_8_1_X64: 3,
    WindowsAppVersion.V5_8_0_X64: 2,
    WindowsAppVersion.V5_9_0_X64: 4,
    WindowsAppVersion.V5_10_7_X64: 8,
    WindowsAppVersion.V5_10_6_X64: 6,
    WindowsAppVersion.V5_10_5_X64: 5,
    WindowsAppVersion.V5_10_4_X64: 4,
    WindowsAppVersion.V5_10_3_X64: 3,
    WindowsAppVersion.V5_10_2_X64: 3,
    WindowsAppVersion.V5_10_1_X64: 2,
    WindowsAppVersion.V5_10_0_X64: 2,
    WindowsAppVersion.V5_11_1_X64: 6,
    WindowsAppVersion.V5_11_0_X64: 4,
    WindowsAppVersion.V5_12_3_X64: 6,
    WindowsAppVersion.V5_12_2_X64: 5,
    WindowsAppVersion.V5_12_1_X64: 4,
    WindowsAppVersion.V5_12_0_X64: 3,
    WindowsAppVersion.V5_13_1_X64: 6,
    WindowsAppVersion.V5_13_0_X64: 4,
    WindowsAppVersion.V5_14_3_X64: 7,
    WindowsAppVersion.V5_14_2_X64: 5,
    WindowsAppVersion.V5_14_1_X64: 4,
    WindowsAppVersion.V5_14_0_X64: 3,
    WindowsAppVersion.V5_15_4_X64: 8,
    WindowsAppVersion.V5_15_3_X64: 6,
    WindowsAppVersion.V5_15_2_X64: 5,
    WindowsAppVersion.V5_15_1_X64: 4,
    WindowsAppVersion.V5_15_0_X64: 3,
    WindowsAppVersion.V5_16_6_X64: 9,
    WindowsAppVersion.V5_16_5_X64: 7,
    WindowsAppVersion.V5_16_4_X64: 6,
    WindowsAppVersion.V5_16_3_X64: 5,
    WindowsAppVersion.V5_16_2_X64: 4,
    WindowsAppVersion.V5_16_1_X64: 3,
    WindowsAppVersion.V5_16_0_X64: 3,
    WindowsAppVersion.V6_0_2_X64: 10,
    WindowsAppVersion.V6_0_1_X64: 7,
    WindowsAppVersion.V6_0_0_X64: 5,
    WindowsAppVersion.V6_1_4_X64: 12,
    WindowsAppVersion.V6_1_3_X64: 10,
    WindowsAppVersion.V6_1_2_X64: 7,
    WindowsAppVersion.V6_1_1_X64: 5,
    WindowsAppVersion.V6_1_0_X64: 4,
    WindowsAppVersion.V6_2_4_X64: 12,
    WindowsAppVersion.V6_2_3_X64: 9,
    WindowsAppVersion.V6_2_2_X64: 6,
    WindowsAppVersion.V6_2_1_X64: 5,
    WindowsAppVersion.V6_2_0_X64: 4,
    WindowsAppVersion.V6_3_9_X64: 14,
    WindowsAppVersion.V6_3_8_X64: 11,
    WindowsAppVersion.V6_3_7_X64: 10,
    WindowsAppVersion.V6_3_6_X64: 8,
    WindowsAppVersion.V6_3_5_X64: 6,
    WindowsAppVersion.V6_3_4_X64: 5,
    WindowsAppVersion.V6_3_3_X64: 4,
    WindowsAppVersion.V6_3_2_X64: 3,
    WindowsAppVersion.V6_3_1_X64: 3,
    WindowsAppVersion.V6_3_0_X64: 3,
    WindowsAppVersion.V6_4_2_X64: 15,
    WindowsAppVersion.V6_4_1_X64: 10,
    WindowsAppVersion.V6_4_0_X64: 7,
    WindowsAppVersion.V6_5_1_X64: 20,
    WindowsAppVersion.V6_5_0_X64: 15,
    WindowsAppVersion.V5_10_0_STORE: 1,
    WindowsAppVersion.V5_15_0_STORE: 1,
    WindowsAppVersion.V6_0_0_STORE: 2,
    WindowsAppVersion.V6_3_0_STORE: 2,
    WindowsAppVersion.V6_5_1_STORE: 3,
}

WINDOWS_SYSTEM_WEIGHTS: Final[Mapping[WindowsSystemVersion, int]] = {
    WindowsSystemVersion.WINDOWS_10_1507: 1,
    WindowsSystemVersion.WINDOWS_10_1511: 1,
    WindowsSystemVersion.WINDOWS_10_1607: 1,
    WindowsSystemVersion.WINDOWS_10_1703: 1,
    WindowsSystemVersion.WINDOWS_10_1709: 1,
    WindowsSystemVersion.WINDOWS_10_1803: 1,
    WindowsSystemVersion.WINDOWS_10_1809: 2,
    WindowsSystemVersion.WINDOWS_10_1903: 2,
    WindowsSystemVersion.WINDOWS_10_1909: 2,
    WindowsSystemVersion.WINDOWS_10_2004: 3,
    WindowsSystemVersion.WINDOWS_10_20H2: 4,
    WindowsSystemVersion.WINDOWS_10_21H1: 5,
    WindowsSystemVersion.WINDOWS_10_21H2: 8,
    WindowsSystemVersion.WINDOWS_10_22H2: 30,
    WindowsSystemVersion.WINDOWS_11_21H2: 5,
    WindowsSystemVersion.WINDOWS_11_22H2: 18,
    WindowsSystemVersion.WINDOWS_11_23H2: 20,
    WindowsSystemVersion.WINDOWS_11_24H2: 14,
    WindowsSystemVersion.WINDOWS_11_25H2: 3,
}

WIN_APPS: Final = tuple(WINDOWS_APP_WEIGHTS.keys())
WIN_APPS_WEIGHTS: Final = tuple(WINDOWS_APP_WEIGHTS.values())

WIN_SYSTEMS: Final = tuple(WINDOWS_SYSTEM_WEIGHTS.keys())
WIN_SYSTEMS_WEIGHTS: Final = tuple(WINDOWS_SYSTEM_WEIGHTS.values())

WINDOWS_COMPATIBILITY_MAP: Final[
    dict[SystemVersion, tuple[tuple[AppVersion, ...], tuple[int, ...]]]
] = get_compatibility_map(OS.WINDOWS, WIN_APPS, WIN_APPS_WEIGHTS, WIN_SYSTEMS)

WINDOWS_DEVICE_MODEL: Final[tuple[WindowsDesktopModel, ...]] = tuple(
    WindowsDesktopModel
)

WINDOWS_WEIGHTS_DT: Final[VersionWeights] = VersionWeights(
    WIN_APPS_WEIGHTS, WIN_SYSTEMS_WEIGHTS
)
