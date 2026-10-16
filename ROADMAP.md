# Source Forensics — Five-Phase Roadmap

## Mission

Determine, with evidence, whether we can build a local-first market-intelligence system that replaces or outperforms the useful capabilities of FastMoss, PiPiADS, Minea and comparable vendors, while minimizing recurring vendor spend.

Source Forensics is not a scraper clone. It is the engineering discipline that answers, for each useful vendor capability:

1. what the feature actually does;
2. what client/backend contract is observable;
3. which fields are raw, historical, derived or modeled;
4. what upstream sources feed it;
5. whether we can reproduce it independently;
6. what it costs to reproduce and maintain;
7. whether our local implementation is good enough to replace the vendor.

Primary objective: build something useful for our own machine and workflows. Commercialization is optional and comes only after internal utility is proven.

## Engineering principles

Normative design baseline: `docs/architecture/ENGINEERING_DESIGN_DOCTRINE.md`. Vendor discoveries are inputs to redesign, not requirements for feature parity.

- Evidence before inference.
- One question per forensic experiment.
- Separate static analysis from runtime observation, then reconcile them.
- Separate active browser scenarios from passive observation; do not overlap them on one target.
- Prefer controlled differential experiments: baseline vs one changed variable.
- Preserve raw artifacts and hashes before interpretation.
- Treat vendor outputs as observations/oracles, not ground truth.
- Prefer upstream official/public sources when they are sufficient, but do not assume they are sufficient before testing.
- REA is a reconnaissance and evidence system; production collectors should use the cheapest deterministic acquisition method that works.
- Every Desktop Commander session ends with durable repository artifacts and a short finding/unknown/next-step report.
- Never make the architecture depend on authentication bypass, stolen sessions, subscription bypass, CAPTCHA/access-control bypass, or third-party credentials.

## Initial specimens

1. FastMoss — first complete specimen; TikTok commerce intelligence.
2. PiPiADS — ad intelligence, historical observation and modeled metrics.
3. Minea — cross-platform ad/product/store relationships.
4. Kalodata — direct comparator for TikTok commerce metrics and schema disagreements.

Later source families are added only after the first end-to-end reproduction succeeds: Amazon/Keepa, Meta, Google, Shopify, Shopee, AliExpress/Alibaba, Temu, YouTube/Instagram/Pinterest and regional marketplaces.

---

# Phase 1 — Forensic laboratory and trustworthy evidence

## Objective

Prove that our NixOS workstation can produce reproducible, trustworthy web-application reverse-engineering evidence with REA 6.5.0 before we draw conclusions about any vendor.

The purpose is not merely to confirm that `rea` runs. The purpose is to establish what evidence we can trust, what the tool cannot observe, what NixOS-specific limitations exist, and how every future experiment must be recorded.

## Work

### A. Record the local toolchain

Record:
- REA version and doctor output;
- Chromium executable and version;
- relevant REA browser/web commands;
- Ghidra/JADX availability for later non-web targets;
- known NixOS support warnings;
- known REA 6.5.0 bugs relevant to evidence interpretation.

### B. Create a disposable forensic browser protocol

Use a dedicated Chromium profile and loopback CDP endpoint. Keep unrelated personal tabs out of the forensic browser.

Two operating modes must be documented:

1. controlled launch mode for reproducible experiments;
2. passive attach mode for observing an already-authenticated, user-owned browser state when required.

### C. Validate the web lane on a harmless target

Validate, one operation at a time:
- `list-browser-targets`;
- `inspect-web-page`;
- `analyze-web-bundle`;
- `capture-browser-scenario`;
- `observe-web-session`;
- `inspect-web-event-listeners`;
- `observe-web-execution`;
- `export-web-scripts`;
- `analyze-javascript-application`;
- `recover-javascript-sources`;
- `trace-web-module-imports`;
- `trace-web-source-location`;
- `inspect-web-network-capture` for retained HAR/mitmproxy evidence;
- capture/screenshot comparison.

### D. Establish evidence discipline

Every capture gets:
- experiment ID;
- target and exact URL/origin;
- timestamp;
- browser/REA version;
- question/hypothesis;
- actions performed;
- raw artifact paths;
- SHA-256 where available;
- limitations and missing evidence;
- analyst conclusion and confidence.

Large raw data is not blindly committed to Git. Git stores manifests, hashes, schemas, scripts and compact evidence needed to reproduce conclusions.

## Exit criteria

Phase 1 ends when we can run a repeatable browser experiment, export the relevant shipped scripts, correlate runtime evidence with static JavaScript evidence, and independently verify artifact identity rather than trusting summary labels alone.

## How Phase 1 can change the project

- If REA web analysis is reliable on this NixOS host: proceed normally.
- If only some lanes are reliable: keep REA for those lanes and supplement with CDP/HAR/mitmproxy directly.
- If REA introduces material instability: isolate it from production and use it strictly as an offline analyzer of retained artifacts.
- If authenticated state cannot be reproduced deterministically: use passive user-owned sessions for observation and separate them from controlled replay.

---

# Phase 2 — Vendor reverse engineering and observable backend reconstruction

## Objective

Reverse engineer FastMoss first, then PiPiADS, Minea and Kalodata, far enough to reconstruct what their clients reveal about the backend contracts and product architecture.

We are not trying to reconstruct private server source code from thin air. We are reconstructing everything legitimately observable from the shipped web client, network behavior, public interfaces, documentation and controlled input/output behavior.

## Unit of work

Never use a vague task such as “reverse engineer FastMoss.”

A forensic unit answers one question, for example:

> What observable backend contract powers `Product Search -> Brazil -> Beauty -> 7 days -> GMV descending`?

For that single question, collect:
- initial page/application state;
- exact action sequence;
- network transactions and request identity where available;
- request method, path/operation and payload shape;
- response schema/shape;
- pagination/cursor behavior;
- entity IDs and relationships;
- filters and enums;
- timestamp/window semantics;
- relevant JS chunks;
- event-listener source locations;
- execution coverage where useful;
- source maps and recovered modules where available;
- client-side calculations and joins;
- evidence references;
- explicit unknowns.

## FastMoss surface order

1. product search/ranking;
2. product detail/history;
3. shops;
4. creators;
5. shoppable videos;
6. LIVE;
7. categories/market views;
8. exports;
9. official API;
10. MCP.

Only after FastMoss yields a coherent graph do we repeat the method on PiPiADS, Minea and Kalodata.

## REA power-user workflow

For each important interaction:

1. Run a controlled scenario to reproduce the action and collect step-indexed network/DOM artifacts.
2. In a separate run, use passive observation while the action is performed to capture initiator/source attribution that controlled scenarios may not expose.
3. Inspect the relevant event listeners.
4. Observe execution coverage only for a focused question.
5. Export captured scripts.
6. Analyze the JavaScript application statically.
7. Recover readable modules when minification/bundling obscures structure.
8. Trace native module imports.
9. Trace selected generated positions through retained source maps.
10. Reconcile static and runtime evidence by digest/identity.
11. Save a retained HAR/mitmproxy capture when transaction-level evidence is important.
12. Run a differential control with exactly one changed input when semantics remain ambiguous.

## Deliverables

Per vendor:
- feature inventory;
- endpoint/operation graph;
- entity graph;
- field dictionary;
- metric definitions;
- client/server derivation hypotheses;
- evidence manifests;
- source-drift observations;
- list of unanswered questions.

## Exit criteria

Phase 2 ends for a vendor when we can explain how its principal user-facing intelligence is represented by the client/backend contract, and when every important field is classified as observed, derived, modeled, historical, third-party or unknown with supporting evidence.

## How Phase 2 can change the project

- If a vendor is mostly a thin wrapper around obvious upstream data, it becomes low priority as an engineering target.
- If it reveals efficient discovery paths, entity relationships or useful refresh strategies, those become upstream hypotheses for Phase 3.
- If a metric exists only as an opaque server-side estimate, it becomes a black-box model-reproduction problem rather than an endpoint-reproduction problem.
- If a vendor contains capabilities we do not actually need, they are dropped instead of cloned.

---

# Phase 3 — Upstream attribution and reproduction feasibility

## Objective

For every high-value vendor capability, identify the most primary sustainable upstream source and determine whether we can reproduce the capability ourselves with acceptable correctness, freshness, maintenance burden and cost.

This is the phase that decides whether building Source Forensics is rational.

## Upstream search order

Evaluate, in order of suitability rather than ideology:

1. official public API/data;
2. official authorized first-party API;
3. official public web surfaces;
4. public structured endpoints used by official clients;
5. deterministic HTTP acquisition;
6. deterministic browser acquisition;
7. licensed third-party data;
8. longitudinal reconstruction from our own snapshots;
9. statistical/model-based estimation.

The first available source is not automatically the best. We compare coverage, terms, geographic scope, freshness, stability, latency and marginal cost.

## Field-level reconstruction

Example:

```text
FastMoss day7_units_sold
  -> define exact observed semantics
  -> identify candidate TikTok primitive(s)
  -> observe primitives longitudinally
  -> test candidate derivations
  -> compare against FastMoss and Kalodata
  -> quantify error, lag and disagreement
  -> determine whether a model is required
```

The same method applies to ad spend estimates, creator-product relationships, first/last-seen dates, rankings and GMV-like metrics.

## Required outputs

- `SourceMap` for each upstream source;
- `CollectorSpec` for each approved primitive;
- field-by-field reproduction matrix;
- cost/freshness/reliability benchmark;
- confidence score for every inferred derivation;
- list of capabilities that are not rational to reproduce.

## Exit criteria

At least one commercially useful vendor metric must be reproduced end-to-end from our own acquisition path with measured error, measured freshness and known cost.

## How Phase 3 can change the project

- If official/public sources already provide nearly everything: Source Forensics becomes mostly an aggregation/history/analytics engine.
- If public primitives exist but vendor value comes from history: prioritize continuous collection immediately.
- If the crucial data requires expensive browser work: benchmark whether the economics still beat the vendor.
- If a valuable capability depends on licensed or genuinely exclusive data: buy, omit or model it rather than pretending we can reproduce it.
- If our reproduction is less accurate or more expensive than buying the vendor, we keep the vendor for that capability.

---

# Phase 4 — Native local market-intelligence engine

## Objective

Implement the capabilities that Phase 3 proved worth owning, using our own collectors, historical data and data-science pipeline. This is where Source Forensics stops being only an investigation repository and begins becoming the local product that replaces vendor usage.

## Acquisition architecture

Separate four responsibilities:

### Discovery
Find new products, sellers, shops, creators, ads, videos, LIVE sessions and relationships.

### Refresh
Revisit known entities at adaptive frequencies based on expected rate of change and value.

### Event capture
Collect short-lived or high-value events where snapshots alone are insufficient.

### Longitudinal snapshots
Append observations over time. Never overwrite previous observations when history is useful.

## Escalation ladder

Use the cheapest deterministic method that preserves required data quality:

```text
L0 official API
L1 structured HTTP
L2 raw HTTP extraction
L3 authorized-session HTTP
L4 deterministic browser
L5 browser + network instrumentation
L6 semantic/agentic browser only when deterministic methods fail
```

REA is removed from the production hot path once the acquisition contract is understood.

## Data architecture

```text
RAW immutable artifacts
    -> append-only OBSERVATIONS
    -> canonical ENTITY GRAPH
    -> DERIVED features
    -> versioned MODELS
    -> SIGNALS / queries / alerts / local API / MCP / UI
```

Candidate local analytical stack to benchmark:
- Parquet;
- Arrow;
- DuckDB;
- Polars/Python;
- R for statistical validation, temporal analysis and model calibration.

Use a separate small control-plane database for jobs/checkpoints if required rather than forcing the analytical store to coordinate collectors.

## Canonical ontology

Vendor-independent entities should include, as needed:
- Product;
- Offer;
- Seller/Shop;
- Creator;
- Video;
- Livestream;
- AdCreative;
- Advertiser;
- Category;
- PriceObservation;
- SalesObservation;
- RankObservation;
- RelationshipObservation.

## Exit criteria

The local system must answer at least one real decision question better or more cheaply than the vendor workflow, using data acquired and processed by us.

Examples:
- which products are accelerating before they enter vendor “trending” pages;
- which creators are beginning to converge on the same product;
- where ad activity, storefront adoption and marketplace sales signals agree;
- which apparent vendor trends disappear when corrected for historical or model bias.

## How Phase 4 can change the project

- If local analytics provides materially better decision quality: expand coverage.
- If collection cost dominates: optimize acquisition before adding more markets.
- If entity resolution is the bottleneck: invest there before more scraping.
- If history is the moat: prioritize continuous reliable snapshots over feature breadth.

---

# Phase 5 — Multi-market expansion and replace/augment/abort decision

## Objective

Determine whether Source Forensics truly replaces the paid intelligence stack, where it only augments it, and where buying external data remains rational.

Only now expand beyond the first TikTok-centered system.

## Expansion families

Add one source family at a time:

1. Amazon + Keepa/Jungle Scout/Helium 10 as reference vendors;
2. Meta commercial/ad transparency surfaces;
3. Google ads/shopping/search signals;
4. Shopify public-store ecosystem plus authorized merchant data where applicable;
5. Shopee;
6. AliExpress/Alibaba ecosystems;
7. Temu;
8. YouTube/Instagram/Pinterest commerce signals;
9. regional marketplaces and Chinese/SEA/LatAm sources as justified by opportunity.

Every new family repeats the same forensic sequence:

```text
vendor/source capability
 -> observable contract
 -> upstream attribution
 -> reproduction benchmark
 -> CollectorSpec
 -> longitudinal collection
 -> analytics validation
```

## Superiority benchmark

For each capability compare:
- coverage;
- correctness/error;
- freshness;
- latency;
- geographic scope;
- historical depth;
- failure rate;
- maintenance burden;
- marginal cost;
- usefulness for actual decisions.

Classify each capability:

- `REPLACE` — our system is sufficient and vendor dependency can be removed;
- `AUGMENT` — combine our data with vendor/external data;
- `BUY` — external data remains economically superior;
- `DROP` — capability is not valuable enough to maintain;
- `MODEL` — direct data is unavailable but estimation is useful.

## Final success criterion

Source Forensics succeeds if it gives us a local, evidence-backed market-intelligence capability whose useful subset is cheaper, more transparent, more customizable or more accurate than relying on FastMoss/PiPiADS/Minea alone.

It does not need to reproduce every button on those products.

If empirical benchmarks show that building a capability is worse than buying it, the correct engineering result is to stop building that capability.

Commercialization is considered only after the local system proves recurring internal value.

---

# Desktop Commander execution contract

Every work session must be small enough to finish cleanly.

A normal session contains:

1. one explicit question;
2. one target/surface;
3. one bounded capture or implementation change;
4. one verification/control;
5. one durable artifact or code change;
6. one commit when the result is coherent;
7. one short report: `FOUND / UNKNOWN / EVIDENCE / NEXT`.

Do not combine in one session:
- two vendors;
- broad reconnaissance and production implementation;
- Nix/REA infrastructure repair and vendor analysis;
- schema redesign and large live captures;
- two unrelated marketplace families.

This discipline is intentional: interrupted reverse-engineering work is only useful when the evidence, assumptions and next question survive the session.

# First execution after this roadmap

Begin Phase 1 with a harmless disposable-browser smoke experiment. Do not point REA at FastMoss until the experiment proves our evidence pipeline and documents the known limitations of REA 6.5.0 on this NixOS host.
