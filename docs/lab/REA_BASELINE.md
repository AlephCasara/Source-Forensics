# REA Laboratory Baseline

Recorded: 2026-10-16
Host: NixOS 26.11

## Installed REA

- Executable: `/etc/profiles/per-user/aleph/bin/rea`
- Version: `6.5.0`
- Node reported by `rea doctor`: `24.21.0`

## Browser

Available commands:

- `/run/current-system/sw/bin/chromium`
- `/run/current-system/sw/bin/chromium-browser`

## REA providers observed by `rea doctor`

### Available

- Ghidra 12.1.2
- Ghidra headless analyzer
- Ghidra native decompiler
- JDK 21
- JADX MCP bridge
- ilspycmd 9.1

### Not configured / unavailable

- Hopper
- IDA MCP registration

These are not blockers for the initial web-application forensics lane.

## Host warning

`rea doctor` currently classifies NixOS 26.11 as `unsupported_host` because REA's host-recognition/setup support targets recognized apt/dnf/pacman families. Individual components can still be healthy, as shown by Ghidra/JADX and the installed CLI.

Source Forensics must therefore validate the exact web lane empirically rather than treating the aggregate doctor status as proof of failure.

Do not run `rea setup` automatically as part of Source Forensics. Agent registration/config drift is an infrastructure concern and should not be mixed with vendor investigations.

## Agent registration drift observed

`rea doctor` reported configuration drift for multiple local agent integrations, including Claude Code, Codex, DSH, Hermes, OMP, OpenCode and Pi.

This does not by itself establish that direct REA CLI web commands are unusable.

## Web-analysis commands confirmed in the installed CLI

- `analyze-javascript-application`
- `analyze-web-bundle`
- `capture-browser-scenario`
- `capture-web-screenshot`
- `compare-web-captures`
- `compare-web-screenshots`
- `discover-webmcp-tools`
- `export-web-scripts`
- `inspect-web-event-listeners`
- `inspect-web-network-capture`
- `inspect-web-page`
- `list-browser-targets`
- `observe-web-execution`
- `observe-web-session`
- `reconcile-javascript-runtime`
- `recover-javascript-sources`
- `trace-javascript-semantics`
- `trace-web-module-imports`
- `trace-web-source-location`

## Known upstream issues relevant to our protocol

At baseline creation time, upstream REA 6.5.0 has recent issue reports relevant to evidence interpretation.

### Script comparison

Issue #3879 reports `compare-web-captures` potentially classifying script content as unchanged despite differing retained source artifact SHA-256 values.

Protocol response: verify script artifact digests directly when script equivalence matters.

### Connected-browser environment

Issue #3395 documents a connect-mode locale inconsistency in which requested locale settings did not fully replace an external browser's existing `navigator.language` state in the reported reproduction.

Protocol response: prefer launch mode for deterministic environment tests and verify effective environment in-page when material.

## Phase 1 next action

Run a harmless disposable-browser smoke experiment that proves:

1. Chromium launches with an isolated profile and loopback CDP;
2. REA lists the target;
3. passive inspection works;
4. a controlled scenario works;
5. scripts can be retained/exported/analyzed;
6. a static/runtime link can be demonstrated;
7. raw evidence and manifests can be stored according to repository policy.

No FastMoss/PiPiADS/Minea capture should begin until this smoke experiment is complete.
