# REA Web Forensics Method

## Purpose

This protocol defines how Source Forensics investigates web applications such as FastMoss, PiPiADS, Minea and Kalodata using REA 6.5.0 and complementary browser/network evidence.

The method is designed to produce defensible engineering conclusions, not endpoint lists without context.

## Core model

Every investigation follows:

```text
QUESTION
  -> HYPOTHESIS
  -> CONTROLLED EXPERIMENT
  -> RAW EVIDENCE
  -> STATIC/RUNTIME CORRELATION
  -> INFERENCE
  -> CONTROL / DIFFERENTIAL TEST
  -> CONCLUSION + CONFIDENCE
```

Do not start from the conclusion and search for confirming artifacts.

## 1. Scope one question

A good question is narrow and falsifiable.

Good:
- Which request is caused by selecting a 7-day GMV sort in FastMoss Product Search?
- Which shipped script registers the click handler for the Product Search filter?
- Is `day7_units_sold` returned by the backend or computed in the browser?
- Does changing only the region alter the endpoint, request body, response schema, or only a parameter?

Bad:
- How does FastMoss work?
- Find all hidden APIs.
- Reverse engineer the backend.

The broad goals are decomposed into many narrow experiments.

## 2. Establish a baseline

Before the target action, record:
- URL/origin;
- visible state;
- relevant selected filters;
- browser version;
- REA version;
- authentication state category without storing credentials;
- experiment timestamp;
- known environmental settings such as locale when material.

For deterministic experiments prefer a disposable browser profile.

## 3. Controlled active scenario

Use `capture-browser-scenario` when REA should perform a fixed sequence of interactions.

Purpose:
- make the action repeatable;
- capture step-indexed results;
- determine which network/DOM changes are associated with each step;
- compare one controlled variant against another.

Use the minimum action sequence required for the question. Add explicit wait steps for the expected stable state rather than relying on timing luck.

Important limitation: scenario network events do not necessarily provide request initiator stacks. Do not infer source-code causality solely from a request appearing in a scenario.

## 4. Separate passive observation

Run a separate passive observation when source attribution matters.

Use:
- `inspect-web-page` for bounded page/network/script evidence;
- `observe-web-session` for a user-driven action window.

The operator performs the action while REA observes.

Do not overlap passive observation and a controlled scenario on the same target. The REA project has demonstrated that overlapping modes can change target state and make attribution unreliable.

Passive observation is especially valuable for request initiator information.

## 5. Event-listener attribution

Use `inspect-web-event-listeners` on the specific UI element when the question is which shipped script handles an interaction.

A listener source is a candidate causal link, not proof that the listener itself sent a particular request.

Correlate it with:
- passive network initiator evidence;
- runtime execution evidence;
- static bundle analysis.

## 6. Focused execution coverage

Use `observe-web-execution` only for narrow questions because it changes runtime instrumentation state by resetting coverage counters and temporarily disabling optimization.

Useful questions:
- Which scripts execute during exactly this action?
- Does this candidate module execute when the filter changes?

Do not treat “script executed” as proof that every function in the script participated.

## 7. Capture and analyze shipped JavaScript

Use `analyze-web-bundle` to identify:
- chunk relationships;
- route candidates;
- endpoint candidates;
- vendor/framework fingerprints;
- source-map evidence where requested.

When script contents are needed, retain them in the capture and use `export-web-scripts`.

Then run `analyze-javascript-application` on the exported files.

The static analysis and runtime evidence are independent evidence sets until reconciled.

## 8. Recover readable module structure

Modern production bundles may be minified or flattened.

Use `recover-javascript-sources` where appropriate to recover more readable modules while preserving provenance.

Never describe recovered output as original source unless the evidence actually establishes original source identity. Recovered modules are analysis artifacts.

## 9. Trace module imports and source maps

Use:
- `trace-web-module-imports` to connect captured scripts to native imports and candidate captured sources;
- `trace-web-source-location` to trace a selected generated position through a retained local source map.

Source maps can dramatically improve understanding of routes, data clients, domain entities and feature code, but absent or partial source maps must remain explicit unknowns.

## 10. Reconcile static and runtime evidence

Use `reconcile-javascript-runtime` only after both evidence sets exist.

Prefer exact digest identity between captured scripts and static artifacts.

Path or URL similarity is weaker evidence. Preserve ambiguity when identities do not match exactly.

A module being present in a runtime-observed bundle does not prove it executed.

## 11. Preserve transaction evidence

For important request/response studies, retain network evidence separately.

REA 6.5.0 supports offline inspection of:
- HAR;
- native mitmproxy captures (with the supported local mitmdump profile);
- Fiddler SAZ;
- qlog where applicable.

Use `inspect-web-network-capture` to analyze retained captures without refetching recorded URLs.

The purpose is to create durable transaction evidence independent of a live browser session.

## 12. Differential experiments

When semantics remain unclear, change one variable at a time.

Examples:

```text
A: region=BR, window=7d, sort=GMV
B: region=US, window=7d, sort=GMV
```

or

```text
A: region=BR, window=7d
B: region=BR, window=28d
```

Compare:
- request path;
- method;
- request fields;
- response schema;
- field values;
- script execution;
- visible result.

Do not change region, category, time window and sort simultaneously if the objective is to learn which parameter controls one of them.

## 13. Classify every conclusion

Use four evidence statuses:

### OBSERVED
Directly present in retained evidence.

Example: response JSON contains `day7_units_sold`.

### DERIVED
Computed deterministically from observed evidence.

Example: a field is produced by an observed client-side function using observed inputs.

### INFERRED
Best explanation supported by multiple observations but not directly visible.

Example: a server-side metric appears to be a rolling historical delta.

### UNKNOWN
Evidence is insufficient or contradictory.

Unknown is an acceptable result. Never upgrade unknown to inferred merely to complete a diagram.

## 14. Confidence

Suggested confidence levels:

- HIGH — repeated direct evidence or a deterministic reconstruction with controls;
- MEDIUM — converging indirect evidence with plausible alternatives substantially reduced;
- LOW — hypothesis supported by limited evidence;
- UNKNOWN — no defensible conclusion.

## 15. Known REA 6.5.0 interpretation rules

### Capture window

Passive network evidence begins after REA attaches. Absence of an earlier request is not evidence that it never happened.

### Active vs passive

Use separate runs. Do not overlap them on one browser target.

### Scenario initiators

Do not assume controlled scenario network records identify the JavaScript initiator. Use passive evidence when initiator attribution is required.

### Compare-web-captures bug

A reported REA 6.5.0 bug can mark the script dimension unchanged even when retained script-source artifact digests differ.

Until fixed/verified locally, compare relevant artifact SHA-256 values directly before accepting “unchanged” for script content.

### Connect-mode environment differences

Connected external browsers can preserve parts of their pre-existing environment. For tightly controlled locale/environment experiments, prefer launch mode and verify the effective page state.

### Secret handling

Do not intentionally put credentials into committed capture artifacts. Keep auth/session values out of repository evidence. Redaction behavior is not a substitute for evidence hygiene.

## 16. Evidence manifest

Every experiment should produce a compact manifest similar to:

```yaml
experiment_id: FM-PRODUCT-SEARCH-001
question: Which request represents a 7-day GMV sort?
target:
  vendor: fastmoss
  surface: product_search
  origin: https://example.invalid
versions:
  rea: 6.5.0
  browser: <recorded>
mode:
  active_scenario: true
  passive_followup: true
artifacts:
  - path: <local raw capture>
    sha256: <digest>
  - path: <exported scripts manifest>
    sha256: <digest>
findings:
  - status: OBSERVED
    statement: <finding>
unknowns:
  - <unresolved question>
confidence: HIGH
next_experiment: <one narrow next question>
```

## 17. Repository rule

Commit:
- methodology;
- compact normalized findings;
- schemas;
- scripts used to reproduce experiments;
- manifests;
- hashes;
- small evidence artifacts when appropriate.

Do not commit by default:
- cookies;
- tokens;
- auth headers;
- browser profiles;
- large raw network captures;
- large screenshots/video dumps;
- unrelated personal browsing state.

## 18. Session rule

Every Desktop Commander session closes with:

```text
FOUND
UNKNOWN
EVIDENCE
NEXT
```

If a conclusion cannot be supported by retained evidence, the session is not complete even if the analyst thinks the conclusion is probably correct.
