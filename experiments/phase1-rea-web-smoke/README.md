# Phase 1 REA Web Smoke Experiment

Controlled experiment validating the Source Forensics REA web workflow before touching a real vendor.

## Ground truth

`fixture/app.js` registers `runMarketSearch` on `#search`. The function creates `region=BR` and `sort=gmv_desc`, fetches `/api/search`, reads JSON, renders two result rows, and writes the returned cursor to the status element.

## Key evidence

- `01-targets.json`: CDP target discovery.
- `02-inspect.json`: baseline passive inspection.
- `04-controlled-scenario.json`: deterministic active scenario.
- `05-listeners.json`: native listener source attribution.
- `07-passive-inspect-long.json`: passive request + initiator + JSON shape.
- `08-bundle-sourcemaps.json`: source-map capture/original-source evidence.
- `09-export-scripts.json`: captured script export.
- `10-static-js-analysis.json`: offline static application graph.
- `11-reconciliation.json`: static/runtime correlation.
- `12-execution.json`: precise execution coverage and request call stack.
- `15-screenshot-diff.json`: visual state change comparison.
- `17-recover-js.json`: Wakaru source recovery.
- `18-source-trace.json`: source-map point trace.

`06-passive-inspect.json` is intentionally retained as a useful negative experiment: its observation timing missed the request. `16-capture-diff.json` records a REA 6.5.0 comparison-contract failure and must not be interpreted as a website failure.

See `../../docs/lab/PHASE1_REA_WEB_LANE_REPORT.md` for conclusions.
