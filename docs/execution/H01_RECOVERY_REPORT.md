# H01 — Recovery audit

Scope: inventory/recovery only; no new browser capture or vendor request.

## Verified local state

- Phase 1 fixture, exported scripts, source maps, `results/01-targets.json` through `results/18-source-trace.json`, and `docs/lab/PHASE1_REA_WEB_LANE_REPORT.md` are tracked and present.
- Existing Phase 1 report records PASS with cautions; this was completed before the hourly roadmap.
- Ports 8765 and 9222 had no listeners at inspection. No process was killed. Other active browser/terminal processes were left untouched because ownership was not established.
- The checkout initially lacked `docs/execution/STATE.md`; during H01 it synchronized with `origin/main` at commit `921434b`. The local tracked tree was clean after sync. Untracked `forensics/upstreams/` belongs to unknown concurrent work and was not touched.
- Existing commits `d868063`, `4b8e569`, `c537eca`, `2d0b251`, `d8f0334` already cover the laboratory and some FastMoss topics. H02–H12 must validate existing evidence before repeating any experiment.

## Independently computed SHA-256

- `fixture/app.js`: `34c219bbd1432ba8b0931921cd6992b7d6e71214d58f7e692607fecf167e8d80`
- `results/04-controlled-scenario.json`: `d331544b9bcb449013051ed70ff71f461a8ef2b2b1a490a7d38c765d4f3ac710`
- `results/05-listeners.json`: `2bb7ade6fdc6d91dbdc889d35313a90c6ad158e4bf18a315dbf942ebcce26fe4`
- `results/07-passive-inspect-long.json`: `7657b29005de14ce1b70600ebab73f03c84efc2afd5c2876ff3fea3004601f70`
- `results/11-reconciliation.json`: `be49d50b38aee6ae68b7612d7328ccf488848b4a39582093ec82f4588ef1047a`
- `results/12-execution.json`: `46a6c06b6f578eca9e1b84f2c0ec966c4217ef8bba0da27ffd4457b5549b421e`
- `results/16-capture-diff.json`: `118d66e1976e04b3129e7a05fd9e6a883cb80aac0766cf35154a9eccca2ce2f6`

`results/16-capture-diff.json` is a typed REA error, not a successful comparison.

## Decision and next

H01 COMPLETE. Preserve existing artifacts; no process cleanup was required. H02 must first verify the already-committed controlled scenario and only re-run it if its exit criterion lacks evidence. Continue one block per scheduled run; do not skip gates based solely on commit titles.

## FOUND

- Existing controlled fixture, REA outputs, and prior Phase 1 report are present on nixos-btw. The prior validation work and FastMoss commits predate the hourly execution plan.
- All 22 artifacts listed in evidence/manifests/phase1-rea-web-smoke.json exist and their independently calculated SHA-256 values match the manifest. No missing or mismatched files.
- Manifest SHA-256: e748c7ec51d347945e17e46066b734a039c0db57b591306c7c8960ff84bdf9a3.
- Fixture server.py, app.js, app.js.map, index.html and scenario.json are present. The scenario launches an isolated Chromium, clicks #search, waits for #results li, and captures network and DOM.
- The seven known prior REA process IDs are absent. No dedicated fixture server or Chromium CDP process was detected; loopback ports 8765 and 9222 refused connections. No process was terminated.
- Local main was fast-forwarded from d8f0334 to 921434b, bringing the hourly roadmap and state into the local clone. Tracked files were clean.
- Pre-existing untracked forensics/upstreams/ remains untouched.

## UNKNOWN

- Whether the old controlled scenario still reproduces with the current runtime. H01 checked stored artifacts, not a fresh capture.
- Ownership of the unrelated untracked upstream directory was not determined; do not stage or delete it.
- Existing docs/lab/PHASE1_REA_WEB_LANE_REPORT.md records a qualified Phase 1 PASS and prior vendor work. The new hourly sequence will revalidate its individual gates without discarding earlier evidence.

## EVIDENCE

- evidence/manifests/phase1-rea-web-smoke.json: 22 independently verified hashes.
- experiments/phase1-rea-web-smoke/results/04-controlled-scenario.json: evidence ev_bf1ab99a5a3c9f487dfeea1a206ea67e3b37d054174f5bc176abe1e460dacec1.
- experiments/phase1-rea-web-smoke/results/05-listeners.json: evidence ev_27ef91c3bbf8ba17bb85837d0132b5199ca0ef60f3d471bb56532aaf29fc48c1.
- experiments/phase1-rea-web-smoke/results/07-passive-inspect-long.json and 12-execution.json.
- experiments/phase1-rea-web-smoke/results/16-capture-diff.json: comparison-contract invalid_request, a documented REA limitation.
- docs/lab/PHASE1_REA_WEB_LANE_REPORT.md: earlier findings and limitations.
- Process inspection: ps of known REA PIDs, pgrep of fixture/CDP, and TCP socket tests on ports 8765 and 9222.

## DECISION

H01 COMPLETE. Preserve all earlier evidence. No stale disposable process needs termination. Keep the unrelated untracked upstream directory untouched. New H02 evidence must use new filenames rather than overwrite the hash-verified records.

## NEXT — H02 only

Start the fixture server on loopback port 8765, run the existing REA scenario in isolated browser launch mode, and verify request /api/search?region=BR&sort=gmv_desc, HTTP 200, two items, cursor-002, and final DOM. Retain a new capture and SHA-256 manifest. Stop only the fixture process started by H02. Do not start H03 in the same run.
