# Priority 7 Device & Performance Telemetry Report

Generated UTC: `2026-11-26T19:15:39Z`

## Tier 4 — Live Windows Desktop Runtime Telemetry (Real SDL2/OpenGL + SDL2 Audio)

| Metric | Measured Value | Notes |
|---|---|---|
| Cold Startup (`app_usable`) | `9118.07` ms | `stages_ms={'build_done': 5778.54, 'on_start': 5779.39, 'splash_ready': 8774.08, 'app_usable': 9118.07}` |
| Time to First Audio (TTFA) | avg `112.017` ms (`n=1`) | DecoderManager + DSPPipeline + SDL2PCMOutput |
| UI Frame Pacing (p50 / p95 / p99 / max) | `29.462 / 2107.399 / 4277.832 / 5111.406` ms | `56` frames, avg `2.24` FPS, missed >16.67ms: `40` (`71.43%`), >33.3ms: `26` |
| Process RAM RSS (baseline / peak / current / delta) | `221.62 / 1132.02 / 1132.02 / 910.4` MiB | `23` RSS samples |
| DSP CPU Load (real-time budget) | `13.081%` | `0.0729s` DSP for `0.5573s` audio (10-band RBJ EQ + Reverb), chunk p95=`21.755` ms |
| Buffer Stalls / Safety | `0` stalls (`0.0s`) | Live audio test played local WAV; remote buffer samples=`0` |
| Network Throughput / Retries | `0` bytes, `0` retries | Stream refreshes=`0` |

### Provider Live Probe Results

- `jiosaavn_search`: ok=`True`, latency=`1157.49` ms, result=`5`, err=`None`
- `youtube_search`: ok=`True`, latency=`1731.86` ms, result=`3`, err=`None`
- `youtube_stream_extract`: ok=`True`, latency=`2581.83` ms, result=`mp4`, err=`None`

## Tier 3 — Android Physical Hardware Probe (`adb`)

- Status: **BLOCKED_APK_NOT_INSTALLED**
- Device: `samsung` `SM-A176B` (`RZCY91AQGKW`), Android SDK `37`, ABIs `arm64-v8a,armeabi-v7a,armeabi`
- APK Installed (`org.shivam.music.kivymusicapp`): `False`
- Blockers: `["Package 'org.shivam.music.kivymusicapp' is not installed on SM-A176B (RZCY91AQGKW).", 'Windows host cannot run `buildozer android debug` (WSL distro not installed).']`
