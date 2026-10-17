# Source Forensics — Execution State

This file is the **single source of truth for scheduled hourly execution**. Every hourly run must read it first and update it last.

## Status

- project_status: ACTIVE
- phase: 1
- current_block: H02
- current_block_title: Controlled browser capture validation (verify existing evidence first)
- next_block_if_success: H03
- execution_mode: ONE_BLOCK_PER_SCHEDULED_RUN
- schedule_intent: HOURLY
- repository: `AlephCasara/Source-Forensics`
- local_repo: `/home/aleph/Projects/Source-Forensics`

## Why H01 was required

Before the hourly execution contract was established, a Phase 1 smoke experiment was started interactively and progressed beyond a clean one-block boundary. Rather than pretend that work was neatly completed, H01 must inventory it, preserve valid evidence, identify stale processes/artifacts, and establish a clean resumable baseline.

## Known pre-roadmap findings to preserve

These findings were observed before the hourly execution model was introduced and must be verified/referenced during H01 rather than silently discarded:

1. REA 6.5.0 is installed on the NixOS workstation.
2. Chromium 154 was successfully launched with a disposable profile and loopback CDP on port 9222.
3. A local controlled fixture existed under `experiments/phase1-rea-web-smoke/fixture/` with a known chain: button -> JS listener -> fetch `/api/search?region=BR&sort=gmv_desc` -> JSON -> DOM update.
4. `rea list-browser-targets` successfully discovered the fixture page.
5. `rea inspect-web-page` and `rea analyze-web-bundle` ran successfully; bundle analysis did not promote the template-string `/api/search?...` construction to an endpoint candidate, demonstrating that static bundle detection alone is insufficient.
6. A controlled `capture-browser-scenario` successfully captured the exact `/api/search?region=BR&sort=gmv_desc` transaction, HTTP 200 response, JSON content and final DOM/result state.
7. `inspect-web-event-listeners` attributed the click listener to `app.js` and captured the exact shipped script source/digest.
8. A passive-observation/execution experiment was started around the time the user interrupted the run. Its processes/results must be inventoried rather than assumed complete.

## H01 scope

H01 may do only the following:

- inspect repository/local experiment state;
- inspect relevant active/stale disposable processes;
- read existing Phase 1 result files;
- identify which pre-roadmap findings have durable evidence;
- stop only disposable forensic processes when safe/necessary;
- create/update a compact Phase 1 recovery report/manifests;
- make the local tree and GitHub state coherent;
- define the exact starting condition for H02.

H01 must **not** start FastMoss or another vendor investigation.
H01 must **not** continue into H02 even if it finishes early.

## Required end-of-run report

Every scheduled run updates this file with:

### FOUND
Concrete verified results from the block.

### UNKNOWN
Questions or incomplete evidence that remain.

### EVIDENCE
Paths, Evidence IDs, hashes, commits, commands or manifests supporting FOUND.

### DECISION
Any architecture/methodology decision justified by the block.

### NEXT
Exactly one next block ID and why it is ready, or `BLOCKED` with recovery action.

## Last transition

- transition: H01 COMPLETE — recovery/inventory verified; H02 queued
- report: `docs/execution/H01_RECOVERY_REPORT.md`

### FOUND
- Tracked Phase 1 fixture, scripts, maps, and results 01–18 are present; prior lab report records PASS with cautions.
- No listener on disposable fixture ports 8765/9222; no process cleanup necessary.
- Local Git synchronized to `921434b`; tracked tree clean. Existing FastMoss commits mean some later hourly topics overlap prior work.

### UNKNOWN
- Ownership of unrelated active sessions and untracked `forensics/upstreams/`; intentionally untouched.
- Whether H02 needs any new capture beyond already-committed evidence.

### EVIDENCE
- `docs/execution/H01_RECOVERY_REPORT.md` with independently computed SHA-256 checks.
- `docs/lab/PHASE1_REA_WEB_LANE_REPORT.md` and `experiments/phase1-rea-web-smoke/results/`.

### DECISION
- Preserve existing evidence; verify before rerunning. No vendor work or new browser capture during H01.

### NEXT
- `H02`: validate existing controlled scenario against its exit criterion; rerun only if missing proof. Do not advance to H03 in the same run.
