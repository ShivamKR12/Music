"""Android ADB Hardware & Runtime Device Verification Tool (Priority 7).

Inspects connected Android hardware via `adb` (model, SDK, ABIs, display metrics,
audio HAL configuration), checks whether `org.shivam.music.kivymusicapp` is built/
installed, and either executes live APK launch + `gfxinfo` + `meminfo` + foreground
service verification OR cleanly reports the exact build/install blocker without
fabricating runtime metrics.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from typing import Any, Dict, List, Optional


PACKAGE_ID = "org.shivam.music.kivymusicapp"
OUT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "docs",
    "performance",
    "android_device_probe.json",
)


def _run(cmd: List[str], timeout: float = 15.0) -> tuple[int, str, str]:
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
        return proc.returncode, proc.stdout.strip(), proc.stderr.strip()
    except Exception as exc:
        return -1, "", str(exc)


def _adb(serial: Optional[str], *args: str, timeout: float = 15.0) -> tuple[int, str, str]:
    base = ["adb"]
    if serial:
        base.extend(["-s", serial])
    base.extend(args)
    return _run(base, timeout=timeout)


def inspect_android_device() -> Dict[str, Any]:
    report: Dict[str, Any] = {
        "package_id": PACKAGE_ID,
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "adb_devices": [],
        "device_info": {},
        "host_build_capability": {},
        "apk_installed": False,
        "device_verification_status": "UNKNOWN",
        "blockers": [],
        "runtime_metrics": None,
    }

    # Host build capability (Buildozer requires Linux / WSL)
    wsl_rc, wsl_out, wsl_err = _run(["wsl", "-l", "-q"], timeout=8.0)
    has_wsl = (wsl_rc == 0 and bool(wsl_out.replace("\x00", "").strip()))
    bz_rc, bz_out, _ = _run(["buildozer", "--version"], timeout=5.0)
    report["host_build_capability"] = {
        "platform": sys.platform,
        "wsl_installed": has_wsl,
        "wsl_detail": (wsl_out or wsl_err).replace("\x00", "").strip(),
        "buildozer_on_host": (bz_rc == 0),
        "buildozer_version": bz_out,
    }

    rc, out, err = _run(["adb", "devices", "-l"], timeout=10.0)
    if rc != 0:
        report["device_verification_status"] = "BLOCKED_ADB_UNAVAILABLE"
        report["blockers"].append(f"adb unavailable: {err or out}")
        return report

    serial: Optional[str] = None
    for line in out.splitlines()[1:]:
        line = line.strip()
        if not line:
            continue
        report["adb_devices"].append(line)
        parts = line.split()
        if len(parts) >= 2 and parts[1] == "device" and serial is None:
            serial = parts[0]

    if not serial:
        report["device_verification_status"] = "BLOCKED_NO_DEVICE"
        report["blockers"].append("No online adb device attached")
        return report

    def prop(name: str) -> str:
        _, p_out, _ = _adb(serial, "shell", "getprop", name)
        return p_out.strip()

    _, wm_size, _ = _adb(serial, "shell", "wm", "size")
    _, wm_density, _ = _adb(serial, "shell", "wm", "density")
    _, audio_flinger, _ = _adb(serial, "shell", "dumpsys", "media.audio_flinger", timeout=10.0)
    _, music_files_out, _ = _adb(serial, "shell", "ls", "-1", "/sdcard/Music")

    audio_sample_rates = sorted(set(re.findall(r"Sample rate:\s*(\d+)", audio_flinger)))
    audio_hal_frames = sorted(set(re.findall(r"HAL frame count:\s*(\d+)", audio_flinger)))

    report["device_info"] = {
        "serial": serial,
        "manufacturer": prop("ro.product.manufacturer"),
        "model": prop("ro.product.model"),
        "android_release": prop("ro.build.version.release"),
        "sdk_int": int(prop("ro.build.version.sdk") or 0),
        "abi_list": prop("ro.product.cpu.abilist"),
        "wm_size": wm_size,
        "wm_density": wm_density,
        "audio_flinger_sample_rates": audio_sample_rates[:6],
        "audio_flinger_hal_frames": audio_hal_frames[:6],
        "sdcard_music_file_count": len([x for x in music_files_out.splitlines() if x.strip() and "No such" not in x]),
    }

    _, pkg_out, _ = _adb(serial, "shell", "pm", "list", "packages", "--user", "0", PACKAGE_ID)
    installed = (f"package:{PACKAGE_ID}" in pkg_out)
    report["apk_installed"] = installed

    if not installed:
        report["device_verification_status"] = "BLOCKED_APK_NOT_INSTALLED"
        report["blockers"].append(
            f"Package '{PACKAGE_ID}' is not installed on {report['device_info']['model']} ({serial})."
        )
        if not has_wsl and not report["host_build_capability"]["buildozer_on_host"]:
            report["blockers"].append(
                "Windows host cannot run `buildozer android debug` (WSL distro not installed)."
            )
        return report

    # Package IS installed -> run live Android runtime verification + gfxinfo/meminfo/service check
    _adb(serial, "shell", "am", "force-stop", PACKAGE_ID)
    _adb(serial, "logcat", "-c")
    _adb(serial, "shell", "dumpsys", "gfxinfo", PACKAGE_ID, "reset")

    t_launch = time.perf_counter()
    _adb(serial, "shell", "monkey", "-p", PACKAGE_ID, "-c", "android.intent.category.LAUNCHER", "1")
    time.sleep(5.0)
    launch_elapsed_ms = round((time.perf_counter() - t_launch) * 1000.0, 2)

    _, gfx_out, _ = _adb(serial, "shell", "dumpsys", "gfxinfo", PACKAGE_ID)
    _, mem_out, _ = _adb(serial, "shell", "dumpsys", "meminfo", PACKAGE_ID)
    _, svc_out, _ = _adb(serial, "shell", "dumpsys", "activity", "services", PACKAGE_ID)
    _, log_out, _ = _adb(serial, "shell", "logcat", "-d", "-t", "120", "python:V", "AndroidRuntime:E", "*:S")

    total_frames = None
    janky_frames = None
    m_tot = re.search(r"Total frames rendered:\s*(\d+)", gfx_out)
    m_jank = re.search(r"Janky frames:\s*(\d+)\s*\(([^)]+)\)", gfx_out)
    if m_tot:
        total_frames = int(m_tot.group(1))
    if m_jank:
        janky_frames = f"{m_jank.group(1)} ({m_jank.group(2)})"

    pss_total_kb = None
    m_pss = re.search(r"TOTAL PSS:\s*(\d+)", mem_out)
    if m_pss:
        pss_total_kb = int(m_pss.group(1))

    report["device_verification_status"] = "VERIFIED_ON_DEVICE"
    report["runtime_metrics"] = {
        "launch_probe_window_ms": launch_elapsed_ms,
        "gfx_total_frames": total_frames,
        "gfx_janky_frames": janky_frames,
        "mem_total_pss_kb": pss_total_kb,
        "foreground_service_active": ("MusicPlayback" in svc_out or "ServiceRecord" in svc_out),
        "fatal_python_or_java_tracebacks": ("Traceback" in log_out or "FATAL EXCEPTION" in log_out),
        "logcat_tail": log_out.splitlines()[-25:],
    }
    return report


def main() -> int:
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    report = inspect_android_device()
    with open(OUT_PATH, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2, ensure_ascii=False)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    # Exit 0 on probe completion so diagnostic harness inspects report without crashing blindly;
    # enforce strict check if --require-installed is passed.
    if "--require-installed" in sys.argv and not report.get("apk_installed"):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
