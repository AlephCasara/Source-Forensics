# Source Forensics

Source Forensics is a local-first reverse-engineering and data-engineering project for determining whether useful market-intelligence capabilities from vendors such as FastMoss, PiPiADS and Minea can be reproduced more transparently, cheaply and flexibly with our own acquisition, history and analytics stack.

The project is not committed to rebuilding every vendor feature. It is committed to measuring which capabilities are worth owning.

## Primary objective

Build a market-intelligence system useful on the local workstation before considering commercialization.

## Current status

Phase 1 is active under a strict hourly execution model. Work is decomposed into bounded blocks; each scheduled run executes exactly one block, persists evidence/code/docs, updates the execution state, and stops. This prevents long Desktop Commander sessions from outrunning ChatGPT's observable work window.

Current execution state lives in [`docs/execution/STATE.md`](docs/execution/STATE.md).

## Read first

- [`ROADMAP.md`](ROADMAP.md) — five-phase project roadmap.
- [`docs/execution/HOURLY_EXECUTION_ROADMAP.md`](docs/execution/HOURLY_EXECUTION_ROADMAP.md) — hour-by-hour bounded execution plan (H01–H86) and tool/session contract.
- [`docs/execution/STATE.md`](docs/execution/STATE.md) — single source of truth for the currently scheduled block and resumable progress.
- [`docs/PROJECT_DECISIONS.md`](docs/PROJECT_DECISIONS.md) — durable record of the major product, reverse-engineering, software and data-architecture decisions made before Phase 1.
- [`docs/architecture/ENGINEERING_DESIGN_DOCTRINE.md`](docs/architecture/ENGINEERING_DESIGN_DOCTRINE.md) — design and engineering doctrine for semantic compression, canonical modeling, provenance, temporal data and software quality.
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
