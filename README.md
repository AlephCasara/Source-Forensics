# Source Forensics

Source Forensics is a local-first reverse-engineering and data-engineering project for determining whether useful market-intelligence capabilities from vendors such as FastMoss, PiPiADS and Minea can be reproduced more transparently, cheaply and flexibly with our own acquisition, history and analytics stack.

The project is not committed to rebuilding every vendor feature. It is committed to measuring which capabilities are worth owning.

## Primary objective

Build a market-intelligence system useful on the local workstation before considering commercialization.

## Current status

Preparation complete for Phase 1. REA 6.5.0 is installed locally, Chromium is available, and the forensic workflow has been defined. The next step is a disposable-browser web-lane smoke experiment before any vendor capture.

## Read first

- [`ROADMAP.md`](ROADMAP.md) — five-phase project roadmap.
- [`docs/methodology/REA_WEB_FORENSICS_METHOD.md`](docs/methodology/REA_WEB_FORENSICS_METHOD.md) — evidence-driven REA web reverse-engineering protocol.
- [`docs/lab/REA_BASELINE.md`](docs/lab/REA_BASELINE.md) — observed local REA/NixOS baseline and known limitations.

## Initial vendor specimens

1. FastMoss
2. PiPiADS
3. Minea
4. Kalodata

## Core rule

For every important capability, Source Forensics must be able to explain the chain:

```text
vendor feature
 -> observable client/backend representation
 -> field semantics
 -> upstream source(s)
 -> acquisition method
 -> historical/derived/model logic
 -> our reproduced value
 -> measured error/freshness/cost/confidence
```

If the external vendor remains technically or economically superior for a capability, the correct result is to keep buying or augmenting that capability rather than cloning it blindly.
