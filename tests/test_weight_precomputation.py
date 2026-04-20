"""Tests for weight_precomputation — WeightCurveParams and compute_weights."""

from typing import Any

import pytest

from tg_devices.enums.android import AndroidAppVersion, AndroidSystemVersion
from tg_devices.enums.linux import LinuxAppVersion, LinuxSystemVersion
from tg_devices.enums.macos import MacOSAppVersion, MacOSSystemVersion
from tg_devices.enums.windows import WindowsAppVersion, WindowsSystemVersion
from tg_devices.weight.introspection.weight_precomputation import (
    PLATFORM_DEFAULTS,
    WeightCurveParams,
    compute_weights,
)


class TestWeightCurveParamsValidation:
    """Test WeightCurveParams field validation."""

    def test_valid_params_do_not_raise(self) -> None:
        """Test that valid parameters construct without errors."""
        params = WeightCurveParams(
            peak_ratio=0.65,
            sigma_left=0.28,
            sigma_right=0.20,
            max_weight=30,
            min_weight=1,
        )
        assert params.peak_ratio == 0.65

    def test_peak_ratio_zero_raises(self) -> None:
        """Test that peak_ratio=0.0 raises ValueError."""
        with pytest.raises(ValueError, match="peak_ratio must be in"):
            WeightCurveParams(peak_ratio=0.0)

    def test_peak_ratio_one_raises(self) -> None:
        """Test that peak_ratio=1.0 raises ValueError."""
        with pytest.raises(ValueError, match="peak_ratio must be in"):
            WeightCurveParams(peak_ratio=1.0)

    def test_peak_ratio_negative_raises(self) -> None:
        """Test that negative peak_ratio raises ValueError."""
        with pytest.raises(ValueError, match="peak_ratio must be in"):
            WeightCurveParams(peak_ratio=-0.1)

    def test_peak_ratio_above_one_raises(self) -> None:
        """Test that peak_ratio > 1 raises ValueError."""
        with pytest.raises(ValueError, match="peak_ratio must be in"):
            WeightCurveParams(peak_ratio=1.5)

    def test_sigma_left_zero_raises(self) -> None:
        """Test that sigma_left=0 raises ValueError."""
        with pytest.raises(ValueError, match="sigma values must be positive"):
            WeightCurveParams(sigma_left=0)

    def test_sigma_right_zero_raises(self) -> None:
        """Test that sigma_right=0 raises ValueError."""
        with pytest.raises(ValueError, match="sigma values must be positive"):
            WeightCurveParams(sigma_right=0)

    def test_sigma_left_negative_raises(self) -> None:
        """Test that negative sigma_left raises ValueError."""
        with pytest.raises(ValueError, match="sigma values must be positive"):
            WeightCurveParams(sigma_left=-0.1)

    def test_max_weight_less_than_min_weight_raises(self) -> None:
        """Test that max_weight < min_weight raises ValueError."""
        with pytest.raises(ValueError, match="max_weight must be"):
            WeightCurveParams(max_weight=1, min_weight=5)

    def test_max_weight_equal_to_min_weight_is_valid(self) -> None:
        """Test that max_weight == min_weight is allowed (flat dist)."""
        params = WeightCurveParams(max_weight=5, min_weight=5)
        assert params.max_weight == params.min_weight

    def test_params_are_frozen(self) -> None:
        """Test that WeightCurveParams instances are immutable."""
        params = WeightCurveParams()
        with pytest.raises((AttributeError, TypeError)):
            params.peak_ratio = 0.5  # type: ignore[misc]


class TestPlatformDefaults:
    """Test PLATFORM_DEFAULTS registry."""

    _EXPECTED_KEYS = {
        "android_app",
        "android_sys",
        "linux_app",
        "linux_sys",
        "macos_app",
        "macos_sys",
        "windows_app",
        "windows_sys",
    }

    def test_all_expected_keys_present(self) -> None:
        """Test that PLATFORM_DEFAULTS contains all eight platform keys."""
        assert set(PLATFORM_DEFAULTS.keys()) == self._EXPECTED_KEYS

    def test_all_values_are_weight_curve_params(self) -> None:
        """Test that every value in PLATFORM_DEFAULTS is WeightCurveParams."""
        for key, value in PLATFORM_DEFAULTS.items():
            assert isinstance(value, WeightCurveParams), (
                f"PLATFORM_DEFAULTS[{key!r}] is not a WeightCurveParams"
            )

    @pytest.mark.parametrize(
        "key",
        ["android_app", "linux_app", "macos_app", "windows_app"],
    )
    def test_app_version_peak_is_below_midpoint(self, key: str) -> None:
        """Test that app version peaks are in the first 65% of the range.

        Users typically lag a few releases behind — the peak should sit
        well before the newest version.
        """
        assert PLATFORM_DEFAULTS[key].peak_ratio <= 0.65, (
            f"{key}: peak_ratio="
            f"{PLATFORM_DEFAULTS[key].peak_ratio} exceeds 0.65"
        )

    @pytest.mark.parametrize(
        "key",
        ["android_sys", "linux_sys", "macos_sys", "windows_sys"],
    )
    def test_sys_version_peak_is_above_midpoint(self, key: str) -> None:
        """Test that system version peaks are in the upper half of the range.

        OS updates are adopted faster — the peak should sit past 0.5.
        """
        assert PLATFORM_DEFAULTS[key].peak_ratio > 0.5, (
            f"{key}: peak_ratio="
            f"{PLATFORM_DEFAULTS[key].peak_ratio} is not > 0.5"
        )

    def test_no_platform_default_has_invalid_params(self) -> None:
        """Test that all platform defaults pass their own validation."""
        for key, params in PLATFORM_DEFAULTS.items():
            assert params.max_weight >= params.min_weight, (
                f"{key}: max_weight < min_weight"
            )
            assert 0 < params.peak_ratio < 1, f"{key}: invalid peak_ratio"
            assert params.sigma_left > 0, f"{key}: sigma_left <= 0"
            assert params.sigma_right > 0, f"{key}: sigma_right <= 0"


class TestComputeWeightsContract:
    """Test the core guarantees of compute_weights."""

    def test_all_members_present_in_result(self) -> None:
        """Test that every enum member appears in the result."""
        result = compute_weights(AndroidAppVersion)
        assert set(result.keys()) == set(AndroidAppVersion)

    def test_all_weights_are_positive(self) -> None:
        """Test that every computed weight is at least 1."""
        result = compute_weights(AndroidAppVersion)
        assert all(w >= 1 for w in result.values())

    def test_all_weights_respect_min_weight(self) -> None:
        """Test that no weight falls below the specified min_weight."""
        min_w = 3
        result = compute_weights(AndroidAppVersion, min_weight=min_w)
        assert all(w >= min_w for w in result.values()), (
            f"Some weights below min_weight={min_w}"
        )

    def test_peak_member_receives_max_weight(self) -> None:
        """Test that the highest weight equals max_weight."""
        max_w = 25
        result = compute_weights(AndroidAppVersion, max_weight=max_w)
        assert max(result.values()) == max_w

    def test_result_weights_are_integers(self) -> None:
        """Test that all returned weights are int, not float."""
        result = compute_weights(AndroidSystemVersion)
        assert all(isinstance(w, int) for w in result.values())

    def test_result_is_deterministic(self) -> None:
        """Test that calling compute_weights twice yields identical results."""
        params = PLATFORM_DEFAULTS["android_app"]
        result1 = compute_weights(AndroidAppVersion, params=params)
        result2 = compute_weights(AndroidAppVersion, params=params)
        assert dict(result1) == dict(result2)

    def test_result_covers_full_weight_range(self) -> None:
        """Test that weights span from min to max (no flat distribution)."""
        params = WeightCurveParams(max_weight=20, min_weight=1)
        result = compute_weights(AndroidAppVersion, params=params)
        assert min(result.values()) < max(result.values())


class TestComputeWeightsSorting:
    """Test that members are sorted by version before weights are assigned."""

    def test_oldest_member_gets_lower_weight_than_mid(self) -> None:
        """Test that the first version gets less weight than mid-range."""
        result = compute_weights(
            AndroidAppVersion, params=PLATFORM_DEFAULTS["android_app"]
        )
        weights = list(result.values())
        first_weight = weights[0]
        mid_weight = weights[len(weights) // 2]
        assert first_weight < mid_weight, (
            f"First member weight {first_weight} >= mid weight {mid_weight}"
        )

    def test_newest_member_gets_lower_weight_than_peak(self) -> None:
        """Test that the latest version has less weight than the peak.

        The right tail drops off steeply — cutting-edge versions are still
        rolling out to users.
        """
        result = compute_weights(
            AndroidAppVersion, params=PLATFORM_DEFAULTS["android_app"]
        )
        weights = list(result.values())
        peak_weight = max(weights)
        last_weight = weights[-1]
        assert last_weight < peak_weight, (
            f"Last member weight {last_weight} >= peak weight {peak_weight}"
        )

    def test_sorted_order_matches_version_order(self) -> None:
        """Test that result keys are in ascending version order."""
        from tg_devices.compatibility.inspection import parse_version

        result = compute_weights(AndroidAppVersion)
        versions = [parse_version(m.value) for m in result]
        assert versions == sorted(versions), (
            "Result keys are not in ascending version order"
        )

    def test_linux_arm64_variants_sorted_with_peers(self) -> None:
        """Test that ARM64 variants sort correctly with their peers."""
        from tg_devices.compatibility.inspection import parse_version

        result = compute_weights(LinuxAppVersion)
        versions = [parse_version(m.value) for m in result]
        assert versions == sorted(versions)


class TestComputeWeightsKeywordOverrides:
    """Test that keyword arguments correctly override params fields."""

    def test_peak_ratio_override_shifts_peak(self) -> None:
        """Test that higher peak_ratio moves peak toward newer versions."""
        base = PLATFORM_DEFAULTS["android_app"]

        result_low = compute_weights(AndroidAppVersion, params=base)
        result_high = compute_weights(
            AndroidAppVersion, params=base, peak_ratio=0.85
        )

        peak_idx_low = list(result_low.values()).index(
            max(result_low.values())
        )
        peak_idx_high = list(result_high.values()).index(
            max(result_high.values())
        )

        assert peak_idx_high > peak_idx_low, (
            "Higher peak_ratio should shift the peak toward newer members"
        )

    def test_max_weight_override_respected(self) -> None:
        """Test that max_weight keyword caps the distribution correctly."""
        result = compute_weights(AndroidAppVersion, max_weight=10)
        assert max(result.values()) == 10

    def test_min_weight_override_respected(self) -> None:
        """Test that min_weight keyword raises the floor."""
        floor = 4
        result = compute_weights(AndroidAppVersion, min_weight=floor)
        assert min(result.values()) >= floor

    def test_keyword_overrides_take_precedence_over_params(self) -> None:
        """Test that an explicit keyword wins over the same field in params."""
        params = WeightCurveParams(max_weight=15)
        result = compute_weights(
            AndroidAppVersion, params=params, max_weight=42
        )
        assert max(result.values()) == 42

    def test_partial_override_leaves_other_fields_intact(self) -> None:
        """Test that overriding one field does not affect the others."""
        params = PLATFORM_DEFAULTS["android_app"]
        result = compute_weights(
            AndroidAppVersion, params=params, max_weight=20
        )
        # min_weight should still be 1 (from params)
        assert min(result.values()) >= params.min_weight

    def test_no_params_uses_default_weight_curve(self) -> None:
        """Test that calling without params falls back to WeightCurveParams."""
        result = compute_weights(AndroidAppVersion)
        default = WeightCurveParams()
        assert max(result.values()) == default.max_weight


class TestComputeWeightsRealEnums:
    """Test compute_weights against all real platform enums."""

    @pytest.mark.parametrize(
        "enum_class,key",
        [
            (AndroidAppVersion, "android_app"),
            (AndroidSystemVersion, "android_sys"),
            (LinuxAppVersion, "linux_app"),
            (LinuxSystemVersion, "linux_sys"),
            (MacOSAppVersion, "macos_app"),
            (MacOSSystemVersion, "macos_sys"),
            (WindowsAppVersion, "windows_app"),
            (WindowsSystemVersion, "windows_sys"),
        ],
    )
    def test_all_members_receive_a_weight(
        self, enum_class: Any, key: str
    ) -> None:
        """Test that every member of a real enum gets a weight assigned."""
        result = compute_weights(enum_class, params=PLATFORM_DEFAULTS[key])
        assert len(result) == len(enum_class)

    @pytest.mark.parametrize(
        "enum_class,key",
        [
            (AndroidAppVersion, "android_app"),
            (AndroidSystemVersion, "android_sys"),
            (LinuxAppVersion, "linux_app"),
            (LinuxSystemVersion, "linux_sys"),
            (MacOSAppVersion, "macos_app"),
            (MacOSSystemVersion, "macos_sys"),
            (WindowsAppVersion, "windows_app"),
            (WindowsSystemVersion, "windows_sys"),
        ],
    )
    def test_no_weight_exceeds_max(self, enum_class: Any, key: str) -> None:
        """Test that no weight exceeds the configured max_weight."""
        params = PLATFORM_DEFAULTS[key]
        result = compute_weights(enum_class, params=params)
        assert max(result.values()) <= params.max_weight, (
            f"{key}: a weight exceeds max_weight={params.max_weight}"
        )

    @pytest.mark.parametrize(
        "enum_class,key",
        [
            (AndroidAppVersion, "android_app"),
            (AndroidSystemVersion, "android_sys"),
            (LinuxAppVersion, "linux_app"),
            (LinuxSystemVersion, "linux_sys"),
            (MacOSAppVersion, "macos_app"),
            (MacOSSystemVersion, "macos_sys"),
            (WindowsAppVersion, "windows_app"),
            (WindowsSystemVersion, "windows_sys"),
        ],
    )
    def test_no_weight_below_min(self, enum_class: Any, key: str) -> None:
        """Test that no weight falls below the configured min_weight."""
        params = PLATFORM_DEFAULTS[key]
        result = compute_weights(enum_class, params=params)
        assert min(result.values()) >= params.min_weight, (
            f"{key}: a weight is below min_weight={params.min_weight}"
        )

    def test_android_app_peak_in_mid_range(self) -> None:
        """Test that Android app version peak sits in the expected range.

        With peak_ratio=0.55 and 33 members, the peak index should be
        near position 17 (0-indexed), i.e. in range [12, 22].
        """
        result = compute_weights(
            AndroidAppVersion, params=PLATFORM_DEFAULTS["android_app"]
        )
        weights = list(result.values())
        peak_idx = weights.index(max(weights))
        n = len(weights)
        assert n * 0.30 <= peak_idx <= n * 0.75, (
            f"Peak at index {peak_idx} is outside expected range for n={n}"
        )

    def test_android_sys_peak_toward_recent(self) -> None:
        """Test that Android system version peak leans toward newer."""
        result = compute_weights(
            AndroidSystemVersion, params=PLATFORM_DEFAULTS["android_sys"]
        )
        weights = list(result.values())
        peak_idx = weights.index(max(weights))
        n = len(weights)
        assert peak_idx >= n * 0.50, (
            f"System peak at {peak_idx} is unexpectedly early for n={n}"
        )


class TestWeightCurveShape:
    """Test that computed weights form a correct asymmetric bell curve.

    The algorithm promises:
    - weights rise from the oldest version up to the peak;
    - weights fall from the peak to the newest version;
    - the right tail (newer) drops faster than the left (older),
      because sigma_right < sigma_left for every platform default.
    """

    @staticmethod
    def _weights(enum_class: Any, key: str) -> list[int]:
        result = compute_weights(enum_class, params=PLATFORM_DEFAULTS[key])
        return list(result.values())

    @staticmethod
    def _peak_idx(weights: list[int]) -> int:
        return weights.index(max(weights))

    @pytest.mark.parametrize(
        "enum_class,key",
        [
            (AndroidAppVersion, "android_app"),
            (AndroidSystemVersion, "android_sys"),
            (WindowsAppVersion, "windows_app"),
            (WindowsSystemVersion, "windows_sys"),
            (MacOSAppVersion, "macos_app"),
            (MacOSSystemVersion, "macos_sys"),
            (LinuxAppVersion, "linux_app"),
            (LinuxSystemVersion, "linux_sys"),
        ],
    )
    def test_left_side_trend_is_rising(
        self, enum_class: Any, key: str
    ) -> None:
        """Test that weights generally increase from oldest to peak.

        We allow minor rounding dips (adjacent weights may be equal)
        but the overall trend must be upward: the average weight of the
        second half of the left side must exceed the first half.
        """
        weights = self._weights(enum_class, key)
        peak = self._peak_idx(weights)
        left = weights[:peak]

        if len(left) < 2:
            pytest.skip("Left side too short to test trend")

        mid = len(left) // 2
        avg_early = sum(left[:mid]) / mid
        avg_late = sum(left[mid:]) / (len(left) - mid)

        assert avg_late > avg_early, (
            f"{key}: left side not rising — "
            f"early avg {avg_early:.1f}, late avg {avg_late:.1f}"
        )

    @pytest.mark.parametrize(
        "enum_class,key",
        [
            (AndroidAppVersion, "android_app"),
            (AndroidSystemVersion, "android_sys"),
            (WindowsAppVersion, "windows_app"),
            (WindowsSystemVersion, "windows_sys"),
            (MacOSAppVersion, "macos_app"),
            (MacOSSystemVersion, "macos_sys"),
            (LinuxAppVersion, "linux_app"),
            (LinuxSystemVersion, "linux_sys"),
        ],
    )
    def test_right_side_trend_is_falling(
        self, enum_class: Any, key: str
    ) -> None:
        """Test that weights generally decrease from peak to newest.

        Same half-split logic as the left-side test, inverted.
        """
        weights = self._weights(enum_class, key)
        peak = self._peak_idx(weights)
        right = weights[peak + 1 :]

        if len(right) < 2:
            pytest.skip("Right side too short to test trend")

        mid = len(right) // 2
        avg_early = sum(right[:mid]) / mid
        avg_late = sum(right[mid:]) / (len(right) - mid)

        assert avg_early > avg_late, (
            f"{key}: right side not falling — "
            f"early avg {avg_early:.1f}, late avg {avg_late:.1f}"
        )

    @pytest.mark.parametrize(
        "enum_class,key",
        [
            (AndroidAppVersion, "android_app"),
            (AndroidSystemVersion, "android_sys"),
            (WindowsAppVersion, "windows_app"),
            (WindowsSystemVersion, "windows_sys"),
            (MacOSSystemVersion, "macos_sys"),
            (LinuxSystemVersion, "linux_sys"),
        ],
    )
    def test_right_tail_drops_faster_than_left(
        self, enum_class: Any, key: str
    ) -> None:
        """Test that the right tail decays faster than the left.

        We compare the drop-per-step on each side:
          left_rate  = (peak_weight - first_weight) / steps_left
          right_rate = (peak_weight - last_weight)  / steps_right

        For sigma_right < sigma_left the right rate must be higher.
        """
        weights = self._weights(enum_class, key)
        peak = self._peak_idx(weights)
        peak_w = weights[peak]

        steps_left = peak
        steps_right = len(weights) - 1 - peak

        if steps_left == 0 or steps_right == 0:
            pytest.skip("Peak at boundary — asymmetry untestable")

        left_rate = (peak_w - weights[0]) / steps_left
        right_rate = (peak_w - weights[-1]) / steps_right

        params = PLATFORM_DEFAULTS[key]
        if params.sigma_right >= params.sigma_left:
            pytest.skip(
                f"{key}: sigma_right >= sigma_left, asymmetry not expected"
            )

        assert right_rate > left_rate, (
            f"{key}: right drop rate {right_rate:.2f} <= "
            f"left drop rate {left_rate:.2f}"
        )
