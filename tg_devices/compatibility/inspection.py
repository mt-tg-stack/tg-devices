"""Semantic version compatibility checks for Telegram clients."""

import re

from tg_devices.enums.os import OS


def parse_version(version_str: str) -> tuple[int, ...]:
    """Extract a numeric version tuple from a version string.

    This function searches for the first dotted-numeric sequence in
    a string (e.g., "10.0.19045") and converts it into a tuple of
    integers for easy comparison. Architecture suffixes like "x64"
    are ignored.

    Args:
        version_str: The raw version string to be parsed.

    Returns:
        A tuple of integers (e.g., (6, 5, 1)). If no numeric sequence
        is found, (0,) is returned.

    """
    match = re.search(r"^v?(\d+(?:\.\d+)*)", version_str.strip())
    if not match:
        raise ValueError(f"Invalid version string: {version_str}")
    return tuple(map(int, match.group(1).split(".")))


def is_compatible(os: OS, sys_ver: str, app_ver: str) -> bool:
    """Check if an app version is compatible with a given OS version.

    This function enforces several real-world and projected
    compatibility rules, such as minimum OS requirements for newer
    app versions and exclusion of legacy apps from modern systems.

    Args:
        os: The target operating system.
        sys_ver: The system version string (e.g., "10.0.22621").
        app_ver: The Telegram app version string (e.g., "5.0.1").

    Returns:
        True if the combination is statistically and technically
        plausible; False otherwise.

    """
    app_v = parse_version(app_ver)
    sys_v = parse_version(sys_ver)

    # 1. User Rule: Telegram Desktop 6.x requires Windows 7+ and macOS 10.13+
    if app_v[0] >= 6:
        if os == OS.WINDOWS:
            # Win 7 is 6.1, Win 10 is 10.0
            if sys_v < (6, 1):
                return False
        elif os == OS.MACOS:
            # macOS 10.13
            if sys_v < (10, 13):
                return False

    # 2. Android Compatibility Rules
    if os == OS.ANDROID:
        # Telegram 10.x requires Android 6.0+
        if app_v[0] >= 10 and sys_v < (6, 0):
            return False
        # Telegram 11.x+ likely requires Android 7.0+ (projected)
        if app_v[0] >= 11 and sys_v < (7, 0):
            return False
        # Telegram 12.x+ likely requires Android 8.0+ (projected)
        if app_v[0] >= 12 and sys_v < (8, 0):
            return False

    # 3. Rule: Old app versions should not appear with new system versions.
    if os == OS.WINDOWS:
        # No 4.x apps on Windows 11+
        if sys_v >= (10, 0, 22000) and app_v < (5, 0):
            return False

    elif os == OS.MACOS:
        # No 4.x apps on Sonoma+
        if sys_v >= (14,) and app_v < (5, 0):
            return False

    elif os == OS.ANDROID:
        # No 8.x/9.x apps on Android 15+
        if sys_v >= (15,) and app_v < (10,):
            return False

    return True
