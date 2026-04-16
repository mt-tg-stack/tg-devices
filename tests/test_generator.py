"""Fixed and stable test suite for DeviceProfileGenerator."""

import pytest

from tg_devices import OS, DeviceProfileGenerator, OSProfile
from tg_devices.compatibility.inspection import is_compatible
from tg_devices.random.provider import StandardRandomProvider


class TestDeviceProfileGeneratorBasic:
    """Test basic profile generation functionality."""

    def test_generate_os_profile(self) -> None:
        """Test that generated profile has valid OS."""
        gen = DeviceProfileGenerator()
        profile = gen.generate_os_profile()

        assert isinstance(profile, OSProfile)
        assert profile.os in [os.value for os in OS]

    def test_generate_specific_os_profile(self) -> None:
        """Test profile generation for specific OS."""
        gen = DeviceProfileGenerator()

        for os_enum in OS:
            profile = gen.generate_os_profile(os=os_enum)
            assert profile.os == os_enum.value


class TestWeightOverrides:
    """Test weight override functionality."""

    def test_weight_overrides_partial_android_bias(self) -> None:
        """Test partial weight override (missing keys auto-filled)."""
        # Provide only android=80, rest is auto-distributed
        gen = DeviceProfileGenerator(android=80)
        android_count = 0
        other_count = 0
        iterations = 1000

        for _ in range(iterations):
            profile = gen.generate_os_profile()
            if profile.os == OS.ANDROID.value:
                android_count += 1
            else:
                other_count += 1

        # Expect significantly more Android profiles
        assert android_count > other_count * 3, (
            f"Android: {android_count}, Others: {other_count}"
        )

    def test_weight_overrides_complete_specification(self) -> None:
        """Test with complete weight specification (all keys provided)."""
        # All weights specified, must sum to 100
        gen = DeviceProfileGenerator(windows=30, macos=15, linux=5, android=50)
        profiles = [gen.generate_os_profile() for _ in range(100)]
        assert len(profiles) == 100

    def test_weight_partial_all_keys_specified(self) -> None:
        """Test that when all keys are specified, no distribution needed."""
        gen = DeviceProfileGenerator(
            windows=40, macos=20, linux=10, android=30
        )
        profiles = [gen.generate_os_profile() for _ in range(100)]
        assert len(profiles) == 100


class TestWeightValidation:
    """Test weight validation."""

    def test_weight_validation_partial_exceeds_100(self) -> None:
        """Test that partial weights exceeding 100 raise ValueError."""
        # windows=50, android=60 = 110 > 100, with missing keys
        with pytest.raises(ValueError, match="Sum of provided weights"):
            DeviceProfileGenerator(windows=50, android=60)

    def test_weight_validation_complete_not_100(self) -> None:
        """Test that complete weights not summing to 100 raise ValueError."""
        # All keys specified but sum != 100
        with pytest.raises(ValueError, match="Weights must sum up to 100"):
            DeviceProfileGenerator(windows=50, macos=30, linux=10, android=5)


class TestSeedConsistency:
    """Test reproducibility with seeds."""

    def test_seed_consistency(self) -> None:
        """Test that same seed produces identical profiles."""
        gen1 = DeviceProfileGenerator(
            random_provider=StandardRandomProvider(seed=42)
        )
        profile1 = gen1.generate_os_profile()

        gen2 = DeviceProfileGenerator(
            random_provider=StandardRandomProvider(seed=42)
        )
        profile2 = gen2.generate_os_profile()

        assert profile1 == profile2

    def test_different_seeds_produce_different_results(self) -> None:
        """Test that different seeds produce different results."""
        gen1 = DeviceProfileGenerator(
            random_provider=StandardRandomProvider(seed=1)
        )
        gen2 = DeviceProfileGenerator(
            random_provider=StandardRandomProvider(seed=2)
        )

        # Generate multiple profiles, they should differ
        profiles1 = [gen1.generate_os_profile() for _ in range(10)]
        profiles2 = [gen2.generate_os_profile() for _ in range(10)]

        assert profiles1 != profiles2


class TestLinuxCompatibility:
    """Test Linux version compatibility."""

    @pytest.mark.parametrize(
        "sys_ver,app_ver",
        [
            ("5.4", "6.0.0"),
            ("5.4", "10.0.0"),
            ("5.4", "11.0.0"),
            ("5.4", "12.0.0"),
            ("5.4", "13.0.0"),
            ("5.4", "14.0.0"),
            ("5.4", "15.0.0"),
        ],
    )
    def test_linux_compatibility_versions(
        self, sys_ver: str, app_ver: str
    ) -> None:
        """Test Linux compatibility for various app versions."""
        assert is_compatible(OS.LINUX, sys_ver, app_ver)


class TestWindowsCompatibility:
    """Test Windows version compatibility."""

    def test_windows_6x_requires_windows_7_plus(self) -> None:
        """Telegram 6.x requires Windows 7+ (6.1)."""
        # Windows Vista (6.0) - too old
        assert not is_compatible(OS.WINDOWS, "6.0", "6.0.0")

        # Windows 7 (6.1) - acceptable
        assert is_compatible(OS.WINDOWS, "6.1", "6.0.0")

        # Windows 10 - acceptable
        assert is_compatible(OS.WINDOWS, "10.0.19041", "6.0.0")

        # Windows 11 - acceptable
        assert is_compatible(OS.WINDOWS, "10.0.22000", "6.0.0")

    def test_windows_old_apps_not_on_new_systems(self) -> None:
        """Test that old apps don't appear on new systems."""
        # No 4.x apps on Windows 11+
        assert not is_compatible(OS.WINDOWS, "10.0.22000", "4.8.0")

    @pytest.mark.parametrize(
        "sys_ver",
        [
            "10.0.19041",  # Windows 10 2004
            "10.0.19042",  # Windows 10 20H2
            "10.0.19043",  # Windows 10 21H1
            "10.0.19044",  # Windows 10 21H2
            "10.0.19045",  # Windows 10 22H2
            "10.0.22000",  # Windows 11
            "10.0.22621",  # Windows 11 22H2
        ],
    )
    def test_windows_10_2004_plus_supports_telegram_6x(
        self, sys_ver: str
    ) -> None:
        """Test that Windows 10 2004+ supports Telegram 6.x."""
        assert is_compatible(OS.WINDOWS, sys_ver, "6.0.0")


class TestMacOSCompatibility:
    """Test macOS version compatibility."""

    def test_macos_6x_requires_10_13_plus(self) -> None:
        """Telegram 6.x requires macOS 10.13+."""
        # macOS Sierra (10.12) - too old
        assert not is_compatible(OS.MACOS, "10.12", "6.0.0")

        # macOS High Sierra (10.13) - acceptable
        assert is_compatible(OS.MACOS, "10.13", "6.0.0")

        # Newer versions - acceptable
        assert is_compatible(OS.MACOS, "10.14", "6.0.0")
        assert is_compatible(OS.MACOS, "11.0", "6.0.0")
        assert is_compatible(OS.MACOS, "14.0", "6.0.0")

    @pytest.mark.parametrize(
        "app_ver",
        [
            "6.0.0",
            "7.0.0",
            "8.0.0",
            "9.0.0",
            "10.0.0",
        ],
    )
    def test_macos_10_13_supports_all_versions(self, app_ver: str) -> None:
        """Test that macOS 10.13+ supports all tested Telegram versions."""
        assert is_compatible(OS.MACOS, "10.13", app_ver)
        assert is_compatible(OS.MACOS, "11.0", app_ver)
        assert is_compatible(OS.MACOS, "14.0", app_ver)

    def test_macos_old_versions_not_supported(self) -> None:
        """Test that old macOS versions don't support new Telegram."""
        # macOS 10.12 doesn't support any tested version
        for app_ver in ["6.0.0", "7.0.0", "8.0.0", "9.0.0", "10.0.0"]:
            assert not is_compatible(OS.MACOS, "10.12", app_ver)


class TestAndroidCompatibility:
    """Test Android version compatibility."""

    def test_android_10x_requires_6_0_plus(self) -> None:
        """Telegram 10.x requires Android 6.0+."""
        # Android 5.0 - too old
        assert not is_compatible(OS.ANDROID, "5.0", "10.0.0")

        # Android 6.0+ - acceptable
        assert is_compatible(OS.ANDROID, "6.0", "10.0.0")
        assert is_compatible(OS.ANDROID, "7.0", "10.0.0")
        assert is_compatible(OS.ANDROID, "15.0", "10.0.0")

    def test_android_11x_requires_7_0_plus(self) -> None:
        """Telegram 11.x requires Android 7.0+."""
        # Android 5.0 and 6.0 - too old
        assert not is_compatible(OS.ANDROID, "5.0", "11.0.0")
        assert not is_compatible(OS.ANDROID, "6.0", "11.0.0")

        # Android 7.0+ - acceptable
        assert is_compatible(OS.ANDROID, "7.0", "11.0.0")
        assert is_compatible(OS.ANDROID, "8.0", "11.0.0")
        assert is_compatible(OS.ANDROID, "15.0", "11.0.0")

    def test_android_12x_requires_8_0_plus(self) -> None:
        """Telegram 12.x requires Android 8.0+."""
        # Android < 8.0 - too old
        assert not is_compatible(OS.ANDROID, "5.0", "12.0.0")
        assert not is_compatible(OS.ANDROID, "6.0", "12.0.0")
        assert not is_compatible(OS.ANDROID, "7.0", "12.0.0")

        # Android 8.0+ - acceptable
        assert is_compatible(OS.ANDROID, "8.0", "12.0.0")
        assert is_compatible(OS.ANDROID, "9.0", "12.0.0")
        assert is_compatible(OS.ANDROID, "15.0", "12.0.0")

    @pytest.mark.parametrize(
        "app_ver",
        [
            "10.0.0",
            "11.0.0",
            "12.0.0",
            "13.0.0",
            "14.0.0",
            "15.0.0",
            "16.0.0",
            "17.0.0",
            "18.0.0",
            "19.0.0",
            "20.0.0",
        ],
    )
    def test_android_15_supports_all_versions(self, app_ver: str) -> None:
        """Test that Android 15 supports all tested Telegram versions."""
        assert is_compatible(OS.ANDROID, "15.0", app_ver)

    def test_android_5_incompatible_with_telegram_10_plus(self) -> None:
        """Test that Android 5.x is incompatible with Telegram 10+."""
        for app_ver in [
            "10.0.0",
            "11.0.0",
            "12.0.0",
            "13.0.0",
            "14.0.0",
            "15.0.0",
        ]:
            assert not is_compatible(OS.ANDROID, "5.0", app_ver)

    @pytest.mark.parametrize(
        "sys_ver,app_ver,expected",
        [
            # Android 5.x
            ("5.0", "9.0.0", True),  # Old app, compatible
            ("5.0", "10.0.0", False),  # Too new app
            # Android 6.x
            ("6.0", "10.0.0", True),  # Exactly at minimum
            ("6.0", "11.0.0", False),  # Requires 7.0
            # Android 7.x
            ("7.0", "11.0.0", True),  # Exactly at minimum
            ("7.0", "12.0.0", False),  # Requires 8.0
            # Android 8.x
            ("8.0", "12.0.0", True),  # Exactly at minimum
            ("8.0", "13.0.0", True),  # Above minimum
            # Modern Android
            ("15.0", "15.0.0", True),  # All compatible
            ("15.0", "20.0.0", True),  # Future versions
        ],
    )
    def test_android_comprehensive_compatibility(
        self, sys_ver: str, app_ver: str, expected: bool
    ) -> None:
        """Test comprehensive Android compatibility matrix."""
        result = is_compatible(OS.ANDROID, sys_ver, app_ver)
        assert result == expected, (
            f"Android {sys_ver} vs Telegram {app_ver}: "
            f"expected {expected}, got {result}"
        )


class TestGeneratedProfilesCompatibility:
    """Test that all generated profiles are compatible."""

    def test_generated_profiles_are_compatible(self) -> None:
        """Test that generated profiles have compatible versions."""
        gen = DeviceProfileGenerator(
            random_provider=StandardRandomProvider(seed=12345)
        )

        # Generate profiles for each OS
        for os_enum in OS:
            for _ in range(50):
                profile = gen.generate_os_profile(os=os_enum)

                result = is_compatible(
                    os_enum,
                    profile.system_version,
                    profile.app_version,
                )

                assert result, f"Generated incompatible profile: {profile}"

    def test_mixed_generation_compatibility(self) -> None:
        """Test that randomly generated profiles are compatible."""
        gen = DeviceProfileGenerator(
            random_provider=StandardRandomProvider(seed=54321)
        )

        for _ in range(200):
            profile = gen.generate_os_profile()

            os_enum = OS(profile.os)
            result = is_compatible(
                os_enum,
                profile.system_version,
                profile.app_version,
            )

            assert result, f"Generated incompatible profile: {profile}"


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_all_os_types_generated(self) -> None:
        """Test that generator can produce profiles for all OSes."""
        gen = DeviceProfileGenerator()
        generated_oses = set()

        for _ in range(500):
            profile = gen.generate_os_profile()
            generated_oses.add(profile.os)

        # Should have generated for at least 2 different OSes
        assert len(generated_oses) >= 2

    def test_profile_immutability(self) -> None:
        """Test that OSProfile instances are immutable."""
        gen = DeviceProfileGenerator()
        profile = gen.generate_os_profile()

        # Should not be able to modify frozen dataclass
        with pytest.raises((AttributeError, TypeError)):
            profile.os = "Modified"  # type: ignore

    def test_single_os_forced_generation(self) -> None:
        """Test forcing generation to single OS."""
        gen = DeviceProfileGenerator(windows=100, macos=0, linux=0, android=0)

        for _ in range(50):
            profile = gen.generate_os_profile()
            assert profile.os == OS.WINDOWS.value

    def test_equal_weight_distribution(self) -> None:
        """Test that equal weights generate all OSes."""
        gen = DeviceProfileGenerator(
            windows=25, macos=25, linux=25, android=25
        )
        generated_oses = set()

        for _ in range(500):
            profile = gen.generate_os_profile()
            generated_oses.add(profile.os)

        # Should generate all 4 OSes with equal weights
        assert len(generated_oses) == 4

    def test_profile_with_forced_os(self) -> None:
        """Test that forcing OS parameter works."""
        gen = DeviceProfileGenerator()

        for os_enum in OS:
            profile = gen.generate_os_profile(os=os_enum)
            assert profile.os == os_enum.value

    def test_multiple_generators_independent(self) -> None:
        """Test that multiple generators are independent."""
        gen1 = DeviceProfileGenerator(android=90)
        gen2 = DeviceProfileGenerator(windows=90)

        profile1 = gen1.generate_os_profile()
        profile2 = gen2.generate_os_profile()

        # They should be independent
        assert isinstance(profile1, OSProfile)
        assert isinstance(profile2, OSProfile)
