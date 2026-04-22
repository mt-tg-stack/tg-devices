"""Core device profile generator implementation."""

import logging
from typing import Unpack

from tg_devices.enums.app_version import AppVersion
from tg_devices.enums.os import OS
from tg_devices.enums.system_version import SystemVersion
from tg_devices.generator.profile import DeviceProfile
from tg_devices.generator.protocols import IDeviceProfileGenerator
from tg_devices.random.protocols import IRandomProvider
from tg_devices.random.provider import StandardRandomProvider
from tg_devices.weight.protocols import IOSProfile, IWeightProvider
from tg_devices.weight.provider import StaticWeightProvider, WeightParams

logger = logging.getLogger(__name__)


class DeviceProfileGenerator(IDeviceProfileGenerator):
    """Generates realistic Telegram client device profiles.

    Combines a randomness provider with a weight provider to produce
    statistically plausible and version-compatible device profiles.

    Args:
        random_provider: Custom randomness source. Defaults to
            ``StandardRandomProvider``.
        weight_provider: Custom weight/data source. Defaults to
            ``StaticWeightProvider``.
        **weight_params: Per-OS weight overrides forwarded to
            ``StaticWeightProvider`` (e.g. ``windows=40, android=60``).

    """

    def __init__(
        self,
        random_provider: IRandomProvider | None = None,
        weight_provider: IWeightProvider | None = None,
        **weight_params: Unpack[WeightParams],
    ) -> None:
        """Initialize the DeviceProfileGenerator
        with optional custom providers and weight parameters.

        Args:
            random_provider: An instance of IRandomProvider to use for random
                selections. If None, a StandardRandomProvider is used.
            weight_provider: An instance of IWeightProvider to provide weights
                and data. If None, a StaticWeightProvider is initialized with
                the provided weight_params.
            **weight_params: Optional keyword arguments to override default OS
                weights in the StaticWeightProvider.

        """
        self._random_provider = random_provider or StandardRandomProvider()
        self._weight_provider = weight_provider or StaticWeightProvider(
            **weight_params
        )

    def _get_compatible_apps(
        self,
        os_profile: IOSProfile,
        system_version: SystemVersion,
    ) -> tuple[tuple[AppVersion, ...], tuple[int, ...]]:
        """Retrieve compatible app versions for a given system version.
        Uses the compatibility map from weights. If the system version is
        not found, falls back to a heuristic selection of apps based on
        weights, or ultimately defaults to all apps with equal weights.

        Args:
            os_profile: OS profile containing compatibility map and app
                weights.
            system_version: The system version for which to find compatible
                apps.

        Returns:
            A tuple of (compatible_apps, compatible_weights) where:
            - compatible_apps: Tuple of AppVersion instances compatible with
                the system version.
            - compatible_weights: Tuple of corresponding weights for the
                compatible apps.

        """
        if system_version in os_profile.compatibility_map:
            return os_profile.compatibility_map[system_version]

        logger.warning(
            f"System version {system_version.value} "
            f"not found in compatibility map."
        )

        fallback_apps, fallback_weights = self._get_fallback_apps(os_profile)
        if fallback_apps:
            logger.warning(
                f"Using fallback app set for system "
                f"version {system_version.value}: "
                f"{len(fallback_apps)} apps selected "
                f"with total weight {sum(fallback_weights)}."
            )
            return fallback_apps, fallback_weights
        logger.warning(
            "No fallback apps found, using all apps with equal weights"
        )
        equal_weights = tuple(1 for _ in os_profile.app_version)
        return os_profile.app_version, equal_weights

    def _get_fallback_apps(
        self,
        os_profile: IOSProfile,
    ) -> tuple[tuple[AppVersion, ...], tuple[int, ...]]:
        """Generate fallback app set when compatibility map is incomplete.

        Strategy: Use the most frequently weighted apps (top 50% by weight).

        Args:
            os_profile: OS profile with app versions and weights.

        Returns:
            Tuple of (fallback_apps, fallback_weights), or empty tuple
            if no apps available.

        """
        if (
            not os_profile.app_version
            or not os_profile.version_weights.app_weights
        ):
            return (), ()

        # Create list of (app, weight) pairs sorted by weight descending
        app_weight_pairs = sorted(
            zip(
                os_profile.app_version,
                os_profile.version_weights.app_weights,
                strict=False,
            ),
            key=lambda x: x[1],
            reverse=True,
        )

        # Calculate cumulative weight threshold (50% of total)
        total_weight = sum(os_profile.version_weights.app_weights)
        threshold = total_weight / 2

        # Accumulate apps until reaching threshold
        selected_apps = []
        selected_weights = []
        cumulative = 0

        for app, weight in app_weight_pairs:
            selected_apps.append(app)
            selected_weights.append(weight)
            cumulative += weight

            if cumulative >= threshold:
                break

        logger.debug(
            f"Fallback apps selected: {len(selected_apps)} out of "
            f"{len(os_profile.app_version)} "
            f"(weight: {cumulative}/{total_weight})"
        )

        return (tuple(selected_apps), tuple(selected_weights))

    def generate_device_profile(
        self,
        os: OS | None = None,
        os_profile: IOSProfile | None = None,
    ) -> DeviceProfile:
        try:
            if os is not None:
                os_names = self._weight_provider.get_os_names()
                if os not in os_names:
                    raise ValueError(
                        f"Specified OS {os!r} is not supported. "
                        f"Available: {os_names!r}"
                    )
                chosen_os = os
            else:
                chosen_os = self._random_provider.choice(
                    population=self._weight_provider.get_os_names(),
                    weights=self._weight_provider.get_os_probabilities(),
                )

            if os_profile is None:
                os_profile = self._weight_provider.get_os_profile(chosen_os)

            system_version = self._random_provider.choice(
                population=os_profile.system_version,
                weights=os_profile.version_weights.system_weights,
            )

            filtered_apps, filtered_weights = self._get_compatible_apps(
                os_profile=os_profile, system_version=system_version
            )

            app_version = self._random_provider.choice(
                population=filtered_apps, weights=filtered_weights
            )

            device_model = self._random_provider.choice(
                population=os_profile.device_model
            )
        except ValueError as e:
            logger.error(f"Error generating profile: {e}")
            raise
        except KeyError as e:
            logger.error(f"Missing data for generation: {e}")
            raise RuntimeError(
                f"Data corruption missing compatibility map for {e}"
            ) from e

        return DeviceProfile(
            os=chosen_os.value,
            app_version=app_version.value,
            system_version=system_version.value,
            device_model=device_model.value,
        )
