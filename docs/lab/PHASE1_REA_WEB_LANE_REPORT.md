# Phase 1 — REA Web-Lane Validation Report

## Status

**PASS with documented cautions.**

Phase 1 established that REA 6.5.0 can be used as the primary web reverse-engineering/evidence instrument on this NixOS host, provided that Source Forensics does not rely on any single REA projection as ground truth and preserves raw evidence, hashes, limitations, and independent cross-checks.

## Controlled fixture

A local HTTP application was created specifically so the true causal chain was known in advance:

```text
#search click
 -> runMarketSearch()
 -> URLSearchParams(region=BR, sort=gmv_desc)
 -> GET /api/search?region=BR&sort=gmv_desc
 -> JSON product records + next_cursor
 -> DOM results render
```

The fixture includes a shipped JavaScript source, a source map, a JSON endpoint, an event listener, asynchronous fetch, and a DOM mutation.

## Results matrix

| Capability | Result | What was proven |
|---|---|---|
| Browser target discovery | PASS | REA discovered the controlled page and exact origin through loopback CDP. |
| Passive page inspection | PASS | DOM/scripts/resources can be inspected without driving the page. |
| Script source capture | PASS | `app.js` bytes were retained with SHA-256 identity. |
| Static bundle analysis | PARTIAL | Asset/chunk was found, but a template-string endpoint was not promoted to an endpoint candidate. Static endpoint discovery must not be treated as complete. |
| Controlled browser scenario | PASS | Click -> fetch -> JSON response -> final DOM state was captured reproducibly. |
| Network body capture | PASS | Controlled scenario retained response content; passive inspection retained value-free JSON shape. |
| Event-listener attribution | PASS | `#search` click listener was located in `app.js` at the expected callback location. |
| Passive request initiator | PASS after timing calibration | Request was attributed to `app.js`, generated line 7, column 25. A shorter first run missed the request; observation windows require explicit timing discipline. |
| Precise execution coverage | PASS | `runMarketSearch` executed once; nested item mapping executed twice; request call stack identified the function and callsite. |
| Source-map fetch | PASS | REA fetched the declared source map and recovered embedded original source content. |
| Script export | PASS | Captured runtime script was exported with manifest and exact SHA-256. |
| Offline JS application analysis | PASS | Exported script parsed into a JavaScript application/semantic graph without execution. |
| Static/runtime reconciliation | PASS | Runtime `app.js` matched static asset by content + mapped location; asset classified `loaded`. |
| JS source recovery | PASS | Wakaru recovery produced derived module/source-map/provenance artifacts; runtime equivalence remains explicitly unknown. |
| Point source-map trace | PASS | Generated callsite mapped to the declared original source line using an explicit local source map. |
| Screenshot capture/comparison | PASS | Before/after screenshots were content-addressed and comparison detected 1,669 changed pixels. |
| `compare-web-captures` on `inspect-web-page` output | CAUTION | REA 6.5.0 CLI rejected inspected passive capture structures while documentation describes passive-capture comparison. Do not depend on this path until contract/version behavior is resolved. |

## Important findings

### 1. Static bundle analysis is not sufficient

The fixture contains an obvious runtime request constructed with a template literal. `inspect-web-page` retained the script text and runtime observation captured the request, but `analyze-web-bundle` did not emit `/api/search` as an endpoint candidate.

Operational rule: **endpoint inventory is the union of static findings, passive runtime observations, controlled scenarios, source analysis, and retained network evidence.** Absence from one detector is never absence from the application.

### 2. Passive capture timing matters

The first short passive window produced zero network requests even though the external action was attempted. Repeating with a longer 12-second window and placing the action well inside the armed interval captured the request and initiator exactly.

Operational rule: for vendor experiments, use an explicit arm -> settle -> action -> settle -> end protocol. Do not fire an action immediately after starting the observer.

### 3. Presence, load, registration, execution, and causality are different claims

The experiment demonstrates distinct evidence levels:

```text
script bytes exist
 != script was loaded
 != listener was registered
 != function executed
 != function caused a specific request
 != UI action caused the business outcome
```

Source Forensics must preserve those distinctions in every VendorDecomposition.

### 4. Runtime-to-static correlation is viable

The captured script SHA-256 matched the exported static artifact, and REA reconciliation classified the asset as loaded using content + URL-prefix mapping. This gives us a practical method for tying FastMoss network behavior to shipped code without conflating source-map declarations with runtime identity.

### 5. Source maps are evidence, not authority

REA can fetch and trace source maps, but source-map authenticity is not independently guaranteed. Original-source names and `sourcesContent` are declarations shipped by the application. They are useful forensic evidence, not proof of server implementation or original repository history.

### 6. Execution coverage perturbs runtime

`observe-web-execution` resets counters and disables optimized execution while armed. Use it for targeted causal questions, not as the default observation mode or performance measurement tool.

## Standard vendor experiment protocol established by Phase 1

1. State one question/hypothesis.
2. Start from a recorded browser/app state.
3. Passive baseline capture.
4. Inspect relevant event listener(s) where practical.
5. Run one controlled scenario to reproduce the UI behavior.
6. Run a separate passive observation with deliberate timing to retain request initiators.
7. Run precise execution coverage only when we need proof that a candidate function executed.
8. Export captured scripts.
9. Analyze static JavaScript offline.
10. Fetch/trace source maps only when useful.
11. Reconcile runtime scripts with static artifacts.
12. Record observations, inferences, unknowns, limitations, hashes, and Evidence IDs separately.
13. Never infer private server code merely from an API contract; use controlled input/output experiments for server-side black-box behavior.

## Phase 1 exit decision

The REA web lane is sufficiently trustworthy to begin FastMoss Vendor Forensics on this host.

Primary operating mode:

```text
REA + dedicated Chromium/CDP
 -> controlled scenario
 -> passive runtime attribution
 -> script export/static analysis
 -> source maps when available
 -> evidence manifests
```

Supplemental tools such as HAR/mitmproxy remain available for traffic retention and cases where REA's bounded capture is insufficient.

## Next bounded question

**FastMoss experiment FM-001:** What public/pre-auth web application architecture is observable from the FastMoss entry surface, and which routes, script chunks, API hosts, application frameworks, and authentication boundaries can be proven before using an authenticated session?
