"""Pre-computation of per-system-version compatibility maps."""

from tg_devices.compatibility.inspection import is_compatible
from tg_devices.enums.app_version import AppVersion
from tg_devices.enums.os import OS
from tg_devices.enums.system_version import SystemVersion


def get_compatibility_map(
    os_name: OS,
    all_apps: tuple[AppVersion, ...],
    all_app_weights: tuple[int, ...],
    all_systems: tuple[SystemVersion, ...],
) -> dict[SystemVersion, tuple[tuple[AppVersion, ...], tuple[int, ...]]]:
    """Build a mapping from each system version to compatible apps.

    For every system version, filters app versions through
    ``is_compatible()`` and pairs them with their weights.

    Args:
        os_name: The target operating system.
        all_apps: All app version enums for this OS.
        all_app_weights: Corresponding selection weights for
            each app version.
        all_systems: All system version enums for this OS.

    Returns:
        Dict mapping each ``SystemVersion`` to a tuple of
        ``(compatible_apps, compatible_weights)``.

    Raises:
        ValueError: If a system version has no compatible app
            versions.

    """
    compat_map: dict[
        SystemVersion, tuple[tuple[AppVersion, ...], tuple[int, ...]]
    ] = {}
    for sys_ver in all_systems:
        compatible = [
            (app_ver, weight)
            for app_ver, weight in zip(all_apps, all_app_weights, strict=False)
            if is_compatible(os_name, sys_ver.value, app_ver.value)
        ]

        if not compatible:
            raise ValueError(
                f"No compatible app versions for"
                f" {os_name.value} {sys_ver.value}"
            )

        filtered_apps = tuple(app for app, _ in compatible)
        filtered_weights = tuple(w for _, w in compatible)

        compat_map[sys_ver] = (filtered_apps, filtered_weights)

    return compat_map
