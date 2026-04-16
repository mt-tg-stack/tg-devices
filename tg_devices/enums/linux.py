"""Linux-specific device model, app version, and system version enums."""

from tg_devices.enums.app_version import AppVersion
from tg_devices.enums.device_model import DeviceModel
from tg_devices.enums.system_version import SystemVersion


class LinuxDesktopModel(DeviceModel):
    """Linux hardware model identifiers (ThinkPads, XPS, Framework, etc.)."""

    THINKPAD_T14_GEN2_AMD = "2166"  # ThinkPad T14 Gen 2 AMD
    THINKPAD_T14S_GEN2_AMD = "216C"  # ThinkPad T14s Gen 2 AMD
    THINKPAD_E14_GEN3 = "2248"  # ThinkPad E14 Gen 3
    THINKPAD_E15_GEN4 = "22CD"  # ThinkPad E15 Gen 4
    THINKPAD_T430S = "2349G5P"  # ThinkPad T430s
    THINKPAD_T530 = "2378DHU"  # ThinkPad T530
    THINKPAD_304BH = "304Bh"
    THINKPAD_3060 = "3060"
    THINKPAD_X13_GEN3 = "30B9"  # ThinkPad X13 Gen 3
    THINKPAD_30DC = "30DC"
    THINKPAD_X13_YOGA_GEN3 = "30F7"  # ThinkPad X13 Yoga Gen 3
    THINKPAD_3600 = "3600"
    THINKPAD_3624 = "3624"
    THINKPAD_3627 = "3627"
    THINKPAD_X1_CARBON_GEN12_CODE = "3642"  # ThinkPad X1 Carbon Gen 12
    THINKPAD_3646H = "3646h"
    THINKPAD_3679CTO = "3679CTO"
    THINKPAD_3717 = "3717"
    THINKPAD_4157RC2 = "4157RC2"
    THINKPAD_4313CTO = "4313CTO"
    THINKPAD_X1_CARBON_GEN4 = "20ATCTO1WW"
    THINKPAD_X1_CARBON_GEN5_A = "20AWA161TH"
    THINKPAD_X1_CARBON_GEN5_B = "20BECTO1WW"
    THINKPAD_T470 = "20HD005EUS"
    THINKPAD_T470S = "20HES2SF00"
    THINKPAD_X1_CARBON_GEN8 = "20V9"
    THINKPAD_X1_YOGA_GEN5 = "20VF"
    THINKPAD_X1_CARBON_GEN9 = "20XW"
    THINKPAD_X1_YOGA_GEN6 = "20XY"
    THINKPAD_T14_GEN3 = "21AH"  # ThinkPad T14 Gen 3
    THINKPAD_T14S_GEN3 = "21AK"  # ThinkPad T14s Gen 3
    THINKPAD_T14_GEN4 = "21BR"  # ThinkPad T14 Gen 4
    THINKPAD_T14S_GEN4 = "21BS"  # ThinkPad T14s Gen 4
    THINKPAD_X1_CARBON_GEN10 = "21CB"  # ThinkPad X1 Carbon Gen 10
    THINKPAD_X1_YOGA_GEN7 = "21CD"  # ThinkPad X1 Yoga Gen 7
    THINKPAD_X1_CARBON_GEN11 = "21E3"  # ThinkPad X1 Carbon Gen 11
    THINKPAD_X1_YOGA_GEN8 = "21E6"  # ThinkPad X1 Yoga Gen 8
    THINKPAD_T14_GEN5 = "21HN"  # ThinkPad T14 Gen 5
    THINKPAD_X1_CARBON_GEN12 = "21ML"  # ThinkPad X1 Carbon Gen 12
    THINKPAD_X1_YOGA_GEN9 = "21MN"  # ThinkPad X1 Yoga Gen 9
    # 2024–2026
    THINKPAD_T14_GEN6 = "21MS"
    THINKPAD_T14S_GEN6 = "21MT"  # ThinkPad T14s Gen 6 AMD
    THINKPAD_X1_CARBON_GEN13 = "21XR"  # ThinkPad X1 Carbon Gen 13 (2025)
    THINKPAD_X1_YOGA_GEN10 = "21XS"  # ThinkPad X1 Yoga Gen 10 (2025)
    THINKPAD_E14_GEN6 = "21M3"  # ThinkPad E14 Gen 6 AMD
    THINKPAD_E16_GEN2 = "21MA"  # ThinkPad E16 Gen 2 AMD
    THINKPAD_L14_GEN5 = "21L1"  # ThinkPad L14 Gen 5 AMD
    THINKPAD_L16_GEN1 = "21L3"  # ThinkPad L16 Gen 1 AMD
    DELL_XPS_13_9310 = "XPS 13 9310"
    DELL_XPS_13_9315 = "XPS 13 9315"
    DELL_XPS_13_9320 = "XPS 13 9320"
    DELL_XPS_13_9340 = "XPS 13 9340"  # 2024 Developer Edition
    DELL_XPS_14_9440 = "XPS 14 9440"
    DELL_XPS_15_9530 = "XPS 15 9530"
    DELL_LATITUDE_5430 = "Latitude 5430"
    DELL_LATITUDE_5440 = "Latitude 5440"
    DELL_LATITUDE_5450 = "Latitude 5450"
    FRAMEWORK_13_AMD_7040 = "Framework Laptop 13 (AMD Ryzen 7040 Series)"
    FRAMEWORK_13_INTEL_13TH = "Framework Laptop 13 (13th Gen Intel Core)"
    FRAMEWORK_13_INTEL_12TH = "Framework Laptop 13 (12th Gen Intel Core)"
    FRAMEWORK_16_AMD_7040 = "Framework Laptop 16 (AMD Ryzen 7040 Series)"
    FRAMEWORK_13_AMD_AI300 = "Framework Laptop 13 (AMD Ryzen AI 300 Series)"
    FRAMEWORK_13_INTEL_ULTRA = (
        "Framework Laptop 13 (Intel Core Ultra Series 1)"
    )
    SYSTEM76_LEMUR_PRO = "Lemur Pro (lemp12)"
    SYSTEM76_ORYX_PRO = "Oryx Pro (oryp12)"
    SYSTEM76_GAZELLE = "Gazelle (gaze20)"
    SYSTEM76_GALAGO_PRO = "Galago Pro (galp7)"
    SYSTEM76_THELIO = "Thelio (thelio-r4)"
    SYSTEM76_MEERKAT = "Meerkat (meer9)"
    TUXEDO_INFINITYBOOK_PRO_14_GEN9 = "TUXEDO InfinityBook Pro 14 Gen9"
    TUXEDO_INFINITYBOOK_PRO_16_GEN9 = "TUXEDO InfinityBook Pro 16 Gen9"
    TUXEDO_PULSE_15_GEN3 = "TUXEDO Pulse 15 Gen3"
    HP_DEV_ONE = "HP Dev One"


class LinuxAppVersion(AppVersion):
    """Telegram Desktop version strings for Linux."""

    V4_8_3 = "4.8.3"
    V4_8_1 = "4.8.1"
    V4_9_9 = "4.9.9"
    V4_9_6 = "4.9.6"
    V4_9_4 = "4.9.4"
    V4_10_4 = "4.10.4"
    V4_10_3 = "4.10.3"
    V4_10_2 = "4.10.2"
    V4_11_6 = "4.11.6"
    V4_11_5 = "4.11.5"
    V4_11_3 = "4.11.3"
    V4_11_2 = "4.11.2"
    V4_12_2 = "4.12.2"
    V4_12_0 = "4.12.0"
    V4_13_1 = "4.13.1"
    V4_13_0 = "4.13.0"
    V4_14_9 = "4.14.9"
    V4_14_4 = "4.14.4"
    V4_14_1 = "4.14.1"
    V4_15_4 = "4.15.4"
    V4_15_2 = "4.15.2"
    V4_15_0 = "4.15.0"
    V4_16_9 = "4.16.9"
    V4_16_8 = "4.16.8"
    V4_16_7 = "4.16.7"
    V4_16_6 = "4.16.6"
    V5_0_4 = "5.0.4"
    V5_0_2 = "5.0.2"
    V5_0_1 = "5.0.1"
    V5_1_9 = "5.1.9"
    V5_1_7 = "5.1.7"
    V5_1_4 = "5.1.4"
    V5_2_3 = "5.2.3"
    V5_2_1 = "5.2.1"
    V5_3_3 = "5.3.3"
    V5_3_2 = "5.3.2"
    V5_3_1 = "5.3.1"
    V5_4_1 = "5.4.1"
    V5_5_5 = "5.5.5"
    V5_5_4 = "5.5.4"
    V5_5_3 = "5.5.3"
    V5_5_2 = "5.5.2"
    V5_5_1 = "5.5.1"
    V5_5_0 = "5.5.0"
    V5_6_3 = "5.6.3"
    V5_6_2 = "5.6.2"
    V5_6_1 = "5.6.1"
    V5_6_0 = "5.6.0"
    V5_7_2 = "5.7.2"
    V5_7_1 = "5.7.1"
    V5_7_0 = "5.7.0"
    V5_8_3 = "5.8.3"
    V5_8_2 = "5.8.2"
    V5_8_1 = "5.8.1"
    V5_8_0 = "5.8.0"
    V5_9_0 = "5.9.0"
    V5_10_7 = "5.10.7"
    V5_10_6 = "5.10.6"
    V5_10_5 = "5.10.5"
    V5_10_4 = "5.10.4"
    V5_10_3 = "5.10.3"
    V5_10_2 = "5.10.2"
    V5_10_1 = "5.10.1"
    V5_10_0 = "5.10.0"
    V5_11_1 = "5.11.1"
    V5_11_0 = "5.11.0"
    V5_12_3 = "5.12.3"
    V5_12_2 = "5.12.2"
    V5_12_1 = "5.12.1"
    V5_12_0 = "5.12.0"
    V5_13_1 = "5.13.1"
    V5_13_0 = "5.13.0"
    V5_14_3 = "5.14.3"
    V5_14_2 = "5.14.2"
    V5_14_1 = "5.14.1"
    V5_14_0 = "5.14.0"
    V5_15_4 = "5.15.4"
    V5_15_3 = "5.15.3"
    V5_15_2 = "5.15.2"
    V5_15_1 = "5.15.1"
    V5_15_0 = "5.15.0"
    V5_16_6 = "5.16.6"
    V5_16_5 = "5.16.5"
    V5_16_4 = "5.16.4"
    V5_16_3 = "5.16.3"
    V5_16_2 = "5.16.2"
    V5_16_1 = "5.16.1"
    V5_16_0 = "5.16.0"
    V6_0_2 = "6.0.2"
    V6_0_1 = "6.0.1"
    V6_0_0 = "6.0.0"
    V6_1_4 = "6.1.4"
    V6_1_3 = "6.1.3"
    V6_1_2 = "6.1.2"
    V6_1_1 = "6.1.1"
    V6_1_0 = "6.1.0"
    V6_2_4 = "6.2.4"
    V6_2_3 = "6.2.3"
    V6_2_2 = "6.2.2"
    V6_2_1 = "6.2.1"
    V6_2_0 = "6.2.0"
    V6_3_9 = "6.3.9"
    V6_3_8 = "6.3.8"
    V6_3_7 = "6.3.7"
    V6_3_6 = "6.3.6"
    V6_3_5 = "6.3.5"
    V6_3_4 = "6.3.4"
    V6_3_3 = "6.3.3"
    V6_3_2 = "6.3.2"
    V6_3_1 = "6.3.1"
    V6_3_0 = "6.3.0"
    V6_4_2 = "6.4.2"
    V6_4_1 = "6.4.1"
    V6_4_0 = "6.4.0"
    V6_5_1 = "6.5.1"
    V6_5_0 = "6.5.0"
    V5_10_0_ARM64 = "5.10.0 arm64"
    V5_15_0_ARM64 = "5.15.0 arm64"
    V6_0_0_ARM64 = "6.0.0 arm64"
    V6_3_0_ARM64 = "6.3.0 arm64"
    V6_5_1_ARM64 = "6.5.1 arm64"


class LinuxSystemVersion(SystemVersion):
    """Linux kernel version strings across major distributions."""

    UBUNTU_20_04_5_4_0_182 = "5.4.0-182-generic"
    UBUNTU_20_04_5_4_0_169 = "5.4.0-169-generic"
    UBUNTU_20_04_5_4_0_155 = "5.4.0-155-generic"
    # Ubuntu 20.04 HWE (Hardware Enablement) kernel 5.15
    UBUNTU_20_04_HWE_5_15_0_112 = "5.15.0-112-generic"
    # ── Ubuntu 22.04 LTS (Jammy) — GA kernel 5.15
    UBUNTU_22_04_5_15_0_127 = "5.15.0-127-generic"
    UBUNTU_22_04_5_15_0_122 = "5.15.0-122-generic"
    UBUNTU_22_04_5_15_0_113 = "5.15.0-113-generic"
    UBUNTU_22_04_5_15_0_100 = "5.15.0-100-generic"
    UBUNTU_22_04_5_15_0_91 = "5.15.0-91-generic"
    # Ubuntu 22.04 HWE kernel 6.5 (ships with 22.04.3+)
    UBUNTU_22_04_HWE_6_5_0_45 = "6.5.0-45-generic"
    UBUNTU_22_04_HWE_6_5_0_28 = "6.5.0-28-generic"
    # Ubuntu 22.04 HWE kernel 6.8 (ships with 22.04.4+)
    UBUNTU_22_04_HWE_6_8_0_52 = "6.8.0-52-generic"
    UBUNTU_22_04_HWE_6_8_0_45 = "6.8.0-45-generic"
    # ── Ubuntu 23.10 (Mantic) — kernel 6.5
    UBUNTU_23_10_6_5_0_27 = "6.5.0-27-generic"
    UBUNTU_23_10_6_5_0_2 = "6.5.0-21-generic"
    # ── Ubuntu 24.04 LTS (Noble) — GA kernel 6.8
    UBUNTU_24_04_6_8_0_57 = "6.8.0-57-generic"
    UBUNTU_24_04_6_8_0_51 = "6.8.0-51-generic"
    UBUNTU_24_04_6_8_0_40 = "6.8.0-40-generic"
    # Ubuntu 24.04 HWE kernel 6.11
    UBUNTU_24_04_HWE_6_11_0_17 = "6.11.0-17-generic"
    UBUNTU_24_04_HWE_6_11_0_13 = "6.11.0-13-generic"
    # ── Ubuntu 24.10 (Oracular) — kernel 6.11
    UBUNTU_24_10_6_11_0_9 = "6.11.0-9-generic"
    # ── Linux Mint 20.x / 21.x (Ubuntu base)
    MINT_21_5_15_0_100 = "5.15.0-100-generic"
    # seen in real Mint forum posts
    MINT_21_2_5_15_0_41 = "5.15.0-41-generic"
    MINT_21_3_6_5_0_35 = "6.5.0-35-generic"
    # ── Debian 10 (Buster) — kernel 4.19
    DEBIAN_10_4_19_0_27 = "4.19.0-27-amd64"
    DEBIAN_10_4_19_0_21 = "4.19.0-21-amd64"
    # ── Debian 11 (Bullseye) — kernel 5.10
    DEBIAN_11_5_10_0_33 = "5.10.0-33-amd64"
    DEBIAN_11_5_10_0_28 = "5.10.0-28-amd64"
    DEBIAN_11_5_10_0_21 = "5.10.0-21-amd64"
    # Debian 11 backport kernel 6.1
    DEBIAN_11_BP_6_1_0_28 = "6.1.0-28-amd64"
    # ── Debian 12 (Bookworm) — kernel 6.1
    DEBIAN_12_6_1_0_30 = "6.1.0-30-amd64"
    DEBIAN_12_6_1_0_27 = "6.1.0-27-amd64"
    DEBIAN_12_6_1_0_21 = "6.1.0-21-amd64"
    DEBIAN_12_6_1_0_18 = "6.1.0-18-amd64"
    # Debian 12 backport kernel 6.12
    DEBIAN_12_BP_6_12_6_1 = "6.12.6-1-amd64"
    # ── Debian 13 (Trixie) — kernel 6.12
    DEBIAN_13_6_12_12_1 = "6.12.12-1-amd64"
    # Seen in real Debian bug report (tdesktop issue #27679 style)
    DEBIAN_SID_5_16_0_5 = "5.16.0-5-amd64"
    ARCH_5_15_74_1 = "5.15.74-1-ARCH"
    ARCH_6_1_1_1 = "6.1.1-1-arch1-1"
    ARCH_6_3_4_ARCH1 = "6.3.4-arch1-1"
    ARCH_6_5_9_ARCH2 = "6.5.9-arch2-1"
    ARCH_6_6_8_ARCH1 = "6.6.8-arch1-1"
    ARCH_6_7_9_ARCH1 = "6.7.9-arch1-1"
    ARCH_6_8_9_ARCH1 = "6.8.9-arch1-1"
    ARCH_6_9_10_ARCH1 = "6.9.10-arch1-1"
    ARCH_6_10_10_ARCH1 = "6.10.10-arch1-1"
    # from real tdesktop bug report #28499
    ARCH_6_11_1_ZEN1 = "6.11.1-zen1-1.1-zen"
    ARCH_6_11_6_ARCH1 = "6.11.6-arch1-1"
    ARCH_6_12_1_ARCH1 = "6.12.1-arch1-1"
    ARCH_6_12_8_ARCH1 = "6.12.8-arch1-1"
    ARCH_6_13_2_ARCH1 = "6.13.2-arch1-1"
    # Fedora 37 — kernel 6.0 / 6.1
    FEDORA_37_6_0_7_301 = "6.0.7-301.fc37.x86_64"
    FEDORA_37_6_1_7_200 = "6.1.7-200.fc37.x86_64"
    # Fedora 38 — kernel 6.2 / 6.3
    FEDORA_38_6_2_9_300 = "6.2.9-300.fc38.x86_64"
    FEDORA_38_6_3_11_300 = "6.3.11-300.fc38.x86_64"
    # Fedora 39 — kernel 6.5 / 6.6
    FEDORA_39_6_5_6_300 = "6.5.6-300.fc39.x86_64"
    FEDORA_39_6_6_14_200 = "6.6.14-200.fc39.x86_64"
    # Fedora 40 — kernel 6.8 / 6.9
    FEDORA_40_6_8_9_300 = "6.8.9-300.fc40.x86_64"
    FEDORA_40_6_9_11_200 = "6.9.11-200.fc40.x86_64"
    # Fedora 41 — kernel 6.11 / 6.12
    FEDORA_41_6_11_4_300 = "6.11.4-300.fc41.x86_64"
    FEDORA_41_6_12_6_200 = "6.12.6-200.fc41.x86_64"
    # Fedora 42 — kernel 6.13
    FEDORA_42_6_13_5_200 = "6.13.5-200.fc42.x86_64"
    MANJARO_5_15_32_1 = "5.15.32-1-MANJARO"
    MANJARO_5_15_85_1 = "5.15.85-1-MANJARO"
    MANJARO_6_1_12_1 = "6.1.12-1-MANJARO"
    MANJARO_6_5_5_1 = "6.5.5-1-MANJARO"
    MANJARO_6_6_30_1 = "6.6.30-1-MANJARO"
    MANJARO_6_9_12_1 = "6.9.12-1-MANJARO"
    MANJARO_6_10_13_1 = "6.10.13-1-MANJARO"
    MANJARO_6_11_3_1 = "6.11.3-1-MANJARO"
    # from tdesktop bug reports 2024
    MANJARO_6_12_4_1 = "6.12.4-1-MANJARO"
    # from MX Linux / Debian-based
    MANJARO_6_12_63_DEB = "6.12.63+deb13-amd64"
    OPENSUSE_LEAP_15_4_5_14_21_150400 = "5.14.21-150400.24.108-default"
    OPENSUSE_LEAP_15_5_5_14_21_150500 = "5.14.21-150500.55.83-default"
    OPENSUSE_LEAP_15_6_6_4_0_150600 = "6.4.0-150600.23.25-default"
    OPENSUSE_TW_6_6_1 = "6.6.1-1-default"
    OPENSUSE_TW_6_8_7 = "6.8.7-1-default"
    OPENSUSE_TW_6_11_3 = "6.11.3-1-default"
    VOID_6_1_12_1 = "6.1.12_1"
    VOID_6_6_8_1 = "6.6.8_1"
    VOID_6_11_5_1 = "6.11.5_1"
    GENTOO_6_1_57 = "6.1.57-gentoo"
    GENTOO_6_6_21 = "6.6.21-gentoo"
    GENTOO_6_6_21_R1 = "6.6.21-gentoo-r1"
    GENTOO_6_12_9 = "6.12.9-gentoo"
    NIXOS_6_1_70 = "6.1.70-nixos"
    NIXOS_6_6_66 = "6.6.66-nixos"
    NIXOS_6_11_8 = "6.11.8-nixos"
    NIXOS_6_12_5 = "6.12.5-nixos"
    MX_21_5_10_0_28 = "5.10.0-28-amd64"  # MX-21 (Debian 11 base)
    MX_23_6_1_0_27 = "6.1.0-27-amd64"  # MX-23 (Debian 12 base)
    POPOS_22_04_6_9_3_76 = "6.9.3-76060903-generic"
    POPOS_22_04_6_8_0_40 = "6.8.0-40-generic"
    POPOS_24_04_6_9_3_76 = "6.9.3-76060903-generic"
    KALI_6_5_0_KALI3 = "6.5.0-kali3-amd64"
    KALI_6_6_9_AMD64 = "6.6.9-amd64"
    KALI_6_11_2_AMD64 = "6.11.2-amd64"
    KALI_6_12_5_AMD64 = "6.12.5-amd64"
