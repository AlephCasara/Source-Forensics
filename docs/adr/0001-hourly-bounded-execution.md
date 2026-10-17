# ADR 0001 — Hourly bounded execution

- Status: Accepted
- Date: 2026-10-16

## Context

Source Forensics is a long, technical reverse-engineering and data-engineering program involving Desktop Commander, REA, Chromium/CDP, retained network evidence, GitHub, multiple vendor specimens, upstream-source analysis, statistical validation and eventual local implementation.

Long interactive runs reduce user observability and can exceed the practical ChatGPT/Desktop Commander work window. A technically successful run is still operationally poor if the user cannot see clean progress boundaries or if state exists only in transient chat/terminal context.

## Decision

Adopt a strict **one bounded block per scheduled hourly run** execution model.

The durable control plane consists of:

- `docs/execution/HOURLY_EXECUTION_ROADMAP.md` — ordered bounded work blocks;
- `docs/execution/STATE.md` — single source of truth for current block and resume state;
- GitHub commits/artifacts — durable evidence and implementation history;
- Desktop Commander — bounded local execution only for the active block.

Each run must:

1. read persistent state first;
2. execute exactly one current block;
3. preserve evidence/code/docs;
4. verify or explicitly mark BLOCKED;
5. update FOUND / UNKNOWN / EVIDENCE / DECISION / NEXT;
6. commit/push coherent work where appropriate;
7. stop before the next block.

If a block proves too large, split it into `Hxx-A/Hxx-B` rather than continuing across the observability boundary.

A ChatGPT automation triggers the continuation hourly. The automation does not define project truth; the GitHub state files do.

## Consequences

### Positive

- user-visible progress at predictable boundaries;
- recoverable work after interruption or chat/context loss;
- evidence and reasoning survive transient tool sessions;
- easier debugging of reverse-engineering mistakes;
- reduced scope creep within individual sessions;
- Git history becomes an execution audit trail;
- vendor and source investigations stay isolated.

### Negative

- some operations that could technically continue immediately must wait for the next block;
- additional state/documentation overhead;
- some blocks may need continuation suffixes when real-world complexity exceeds estimates.

## Rejected alternatives

### Continuous long-running ChatGPT/Desktop Commander sessions
Rejected because they reduce observability, increase interruption risk and encourage scope expansion.

### Time-box only, without persistent state
Rejected because elapsed time does not guarantee resumability or evidence preservation.

### Let each agent decide scope dynamically
Rejected because dynamic scope expansion produced the exact observability failure this ADR addresses.

## Review trigger

Review this ADR only if the execution platform provides a substantially larger reliable observable work window while preserving interruption-safe state. Even then, persistent GitHub checkpoints remain required.
