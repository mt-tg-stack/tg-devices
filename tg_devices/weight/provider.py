"""Static weight provider implementation."""

import logging
from typing import TypedDict, Unpack, cast

from tg_devices.enums.os import OS
from tg_devices.weight.introspection import (
    ANDROID_APP_VERSIONS,
    ANDROID_APP_WEIGHTS,
    ANDROID_COMPATIBILITY_MAP,
    ANDROID_DEVICE_MODELS,
    ANDROID_SYSTEM_VERSIONS,
    ANDROID_SYSTEM_WEIGHTS,
    ANDROID_WEIGHTS_DATA,
    LINUX_APP_VERSIONS,
    LINUX_APP_WEIGHTS,
    LINUX_COMPATIBILITY_MAP,
    LINUX_DEVICE_MODELS,
    LINUX_SYSTEM_VERSIONS,
    LINUX_SYSTEM_WEIGHTS,
    LINUX_WEIGHTS_DATA,
    MACOS_APP_VERSIONS,
    MACOS_APP_WEIGHTS,
    MACOS_COMPATIBILITY_MAP,
    MACOS_DEVICE_MODELS,
    MACOS_SYSTEM_VERSIONS,
    MACOS_SYSTEM_WEIGHTS,
    MACOS_WEIGHTS_DATA,
    OS_NAMES,
    WINDOWS_APP_VERSIONS,
    WINDOWS_APP_WEIGHTS,
    WINDOWS_COMPATIBILITY_MAP,
    WINDOWS_DEVICE_MODELS,
    WINDOWS_SYSTEM_VERSIONS,
    WINDOWS_SYSTEM_WEIGHTS,
    WINDOWS_WEIGHTS_DATA,
)
from tg_devices.weight.protocols import IOSProfile, IWeightProvider
from tg_devices.weight.weights import OSProfile

logger = logging.getLogger(__name__)


class WeightParams(TypedDict, total=False):
    """Per-OS weight overrides for ``StaticWeightProvider``.

    All keys are optional. Provided weights must sum to <= 100;
    missing OS weights are distributed proportionally from the
    remaining budget.

    Attributes:
        windows: Weight for Windows (default 30).
        linux: Weight for Linux (default 5).
        macos: Weight for macOS (default 15).
        android: Weight for Android (default 50).

    """

    windows: int
    linux: int
    macos: int
    android: int


class StaticWeightProvider(IWeightProvider):
    """Provides pre-computed weight distributions for each OS.

    Uses static introspection data (version enums, weight mappings,
    compatibility maps) and builds per-instance ``StaticOSWeights``
    bundles based on the supplied weight parameters.

    Args:
        **weight_params: Per-OS weight overrides. Omitted OS weights
            are distributed proportionally from the remaining budget.
            All weights must sum to 100.

    Raises:
        ValueError: If provided weights sum to >= 100 with missing
            keys, or if final weights do not sum to 100.

    """

    windows_apps = WINDOWS_APP_VERSIONS
    windows_systems = WINDOWS_SYSTEM_VERSIONS
    macos_apps = MACOS_APP_VERSIONS
    macos_systems = MACOS_SYSTEM_VERSIONS
    linux_apps = LINUX_APP_VERSIONS
    linux_systems = LINUX_SYSTEM_VERSIONS
    android_apps = ANDROID_APP_VERSIONS
    android_systems = ANDROID_SYSTEM_VERSIONS
    windows_app_weights = WINDOWS_APP_WEIGHTS
    windows_system_weights = WINDOWS_SYSTEM_WEIGHTS
    macos_app_weights = MACOS_APP_WEIGHTS
    macos_system_weights = MACOS_SYSTEM_WEIGHTS
    linux_app_weights = LINUX_APP_WEIGHTS
    linux_system_weights = LINUX_SYSTEM_WEIGHTS
    android_app_weights = ANDROID_APP_WEIGHTS
    android_system_weights = ANDROID_SYSTEM_WEIGHTS
    os_names = OS_NAMES
    windows_compatibility_map = WINDOWS_COMPATIBILITY_MAP
    macos_compatibility_map = MACOS_COMPATIBILITY_MAP
    linux_compatibility_map = LINUX_COMPATIBILITY_MAP
    android_compatibility_map = ANDROID_COMPATIBILITY_MAP
    windows_device_model = WINDOWS_DEVICE_MODELS
    macos_device_model = MACOS_DEVICE_MODELS
    linux_device_model = LINUX_DEVICE_MODELS
    android_device_model = ANDROID_DEVICE_MODELS
    windows_weights_dt = WINDOWS_WEIGHTS_DATA
    macos_weights_dt = MACOS_WEIGHTS_DATA
    linux_weights_dt = LINUX_WEIGHTS_DATA
    android_weights_dt = ANDROID_WEIGHTS_DATA

    @staticmethod
    def _distribute_weights_lrm(
        remaining: int,
        missing_keys: list[str],
        defaults: dict[str, int],
    ) -> dict[str, int]:
        """Distribute remaining weight using Largest Remainder Method.

        This method ensures that:
        1. All weights sum exactly to the remaining budget
        2. Distribution is as close as possible to the default proportions
        3. No rounding errors accumulate

        Algorithm (Hare-Niemeyer / Largest Remainder):
        1. Calculate base allocation: floor(remaining * proportion)
        2. Calculate remainder for each key: fractional part
        3. Distribute remaining quota to keys with largest remainders

        Args:
            remaining: Total weight budget to distribute.
            missing_keys: List of keys that need weight allocation.
            defaults: Default weight for each key (for proportion calculation).

        Returns:
            Dictionary with distributed weights summing to exactly `remaining`.

        """
        distribution: dict[str, int] = {}
        total_default = sum(defaults[k] for k in missing_keys)

        if total_default == 0:
            logger.warning(
                f"All default weights for missing keys {missing_keys}"
                f" are 0. Distributing equally."
            )
            # Edge case: all defaults are 0, distribute equally
            base_allocation = remaining // len(missing_keys)
            extra = remaining % len(missing_keys)
            for i, key in enumerate(missing_keys):
                distribution[key] = base_allocation + (1 if i < extra else 0)
            return distribution

        # Step 1: Calculate base allocation and fractional parts
        allocations: dict[str, float] = {}
        base_allocations: dict[str, int] = {}
        fractional_parts: dict[str, float] = {}

        for key in missing_keys:
            proportion = defaults[key] / total_default
            exact_allocation = remaining * proportion
            base = int(exact_allocation)  # floor division

            allocations[key] = exact_allocation
            base_allocations[key] = base
            fractional_parts[key] = exact_allocation - base

        total_base = sum(base_allocations.values())
        quota_remaining = remaining - total_base

        # Step 2: Sort by fractional part (descending) and distribute remainder
        # Keys with larger fractional parts get priority
        sorted_by_remainder = sorted(
            missing_keys,
            key=lambda k: fractional_parts[k],
            reverse=True,
        )

        for i in range(quota_remaining):
            lucky_key = sorted_by_remainder[i]
            base_allocations[lucky_key] += 1

        return base_allocations

    def __init__(self, **weight_params: Unpack[WeightParams]) -> None:
        """Initialize the StaticWeightProvider with optional weight parameters.
        The constructor builds the internal mapping of OS to StaticOSWeights
        based on the provided weights and the static introspection data.

        Args:
            **weight_params: Optional per-OS weight overrides. Keys can be

        """  # noqa: D205
        defaults = {"windows": 30, "macos": 15, "linux": 5, "android": 50}
        weights: dict[str, int]
        if not weight_params:
            weights = dict(defaults)
        else:
            weights = cast(dict[str, int], dict(weight_params))

        missing_keys = [k for k in defaults if k not in weights]

        if missing_keys:
            provided_sum = sum(weights.values())
            if provided_sum > 100:
                raise ValueError(
                    f"Sum of provided weights ({provided_sum})"
                    f" is > 100, but keys {missing_keys} are missing."
                )

            remaining = 100 - provided_sum

            # Use Largest Remainder Method for distribution
            distributed = self._distribute_weights_lrm(
                remaining, missing_keys, defaults
            )
            weights.update(distributed)

        if sum(weights.values()) != 100:
            raise ValueError(
                f"Weights must sum up to 100, got {sum(weights.values())}"
            )

        self.map = {
            OS.WINDOWS: OSProfile(
                app_version=self.windows_apps,
                system_version=self.windows_systems,
                device_model=self.windows_device_model,
                selection_weight=weights["windows"],
                version_weights=self.windows_weights_dt,
                compatibility_map=self.windows_compatibility_map,
            ),
            OS.MACOS: OSProfile(
                app_version=self.macos_apps,
                system_version=self.macos_systems,
                device_model=self.macos_device_model,
                selection_weight=weights["macos"],
                version_weights=self.macos_weights_dt,
                compatibility_map=self.macos_compatibility_map,
            ),
            OS.LINUX: OSProfile(
                app_version=self.linux_apps,
                system_version=self.linux_systems,
                device_model=self.linux_device_model,
                selection_weight=weights["linux"],
                version_weights=self.linux_weights_dt,
                compatibility_map=self.linux_compatibility_map,
            ),
            OS.ANDROID: OSProfile(
                app_version=self.android_apps,
                system_version=self.android_systems,
                device_model=self.android_device_model,
                selection_weight=weights["android"],
                version_weights=self.android_weights_dt,
                compatibility_map=self.android_compatibility_map,
            ),
        }
        self.os_probabilities: tuple[int, ...] = tuple(
            weight.selection_weight for weight in self.map.values()
        )

    def get_os_profile(self, os: OS) -> IOSProfile:
        return self.map[os]

    def get_os_names(self) -> tuple[OS, ...]:
        return self.os_names

    def get_os_probabilities(self) -> tuple[int, ...]:
        return self.os_probabilities
