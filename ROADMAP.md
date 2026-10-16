# Source Forensics — Reverse-Engineering Roadmap

## Mission

Build a local-first market-intelligence system that can replace or outperform selected capabilities of FastMoss, PiPiADS, Minea, and comparable vendors by combining:

1. reverse engineering of observable vendor clients/backends;
2. upstream source attribution;
3. first-party collectors;
4. longitudinal storage;
5. entity resolution;
6. reproducible derivations and statistical models;
7. continuous validation against vendors and official sources.

The target is not a scraper clone. The target is a source-to-signal data system.

## Operating constraints

- Prefer official/public upstream sources whenever they are sufficient.
- Use authorized accounts/sessions only where authentication is required.
- Do not design around authentication bypass, subscription bypass, stolen credentials, or access-control circumvention.
- REA is a reconnaissance/evidence tool, not the production collector runtime.
- Every Desktop Commander work unit must end with durable artifacts in this repository.
- Do not run `rea setup` automatically on this NixOS host; REA integration drift is handled separately from Source Forensics.

## Reverse-engineering model

For every vendor capability, reconstruct this chain:

```text
Vendor feature
  -> client representation
  -> observable backend contract
  -> field semantics
  -> upstream-source candidates
  -> acquisition method
  -> historical requirement
  -> derivation/model requirement
  -> independent implementation
  -> validation
```

A backend is treated as two layers:

- **observable backend contract**: endpoints, GraphQL operations, schemas, IDs, pagination, filters, batching, error semantics, caching clues, WebSockets, client-side joins, feature flags;
- **private server implementation**: inferred only from controlled input/output behavior when it is not shipped to the client.

## Initial target order

### Wave 1 — TikTok commerce / ad intelligence

1. **FastMoss** — primary specimen and first end-to-end reproduction study.
2. **PiPiADS** — ad-intelligence and modeled-metric specimen.
3. **Minea** — cross-platform ad/product/store graph specimen.
4. **Kalodata** — direct FastMoss comparator; useful for consensus/disagreement analysis and API-contract comparison.

### Wave 2 — Different source archetypes

5. **Keepa** — Amazon historical-price/rank/data-API archetype.
6. **Jungle Scout or Helium 10** — Amazon market-estimation archetype.
7. **Similarweb** — later, model-heavy traffic/intelligence archetype.

Shoplus/EchoTik/other TikTok analytics vendors are reserve targets: use them when an additional independent vendor is needed to arbitrate a disputed field or acquisition hypothesis.

---

# Phase 0 — Laboratory readiness

## Goal

Prove that the REA web-analysis lane works reliably on this NixOS host without changing global configuration.

## Desktop Commander work units

### 0.1 REA baseline

Record:
- `rea --version`;
- `rea doctor`;
- relevant browser/CDP commands present;
- browser executable(s);
- Playwright/Chromium availability.

Artifact:
- `docs/lab/REA_BASELINE.md`

### 0.2 Disposable forensic browser

Validate a dedicated Chromium-family profile with loopback CDP and no unrelated personal tabs.

Artifact:
- `docs/lab/BROWSER_FORENSICS_PROTOCOL.md`

### 0.3 REA web-lane smoke test

Against a harmless public site, validate:
- target listing;
- page inspection;
- bundle analysis;
- script export;
- bounded session observation;
- evidence export;
- capture comparison.

Artifact:
- `experiments/rea-web-smoke/`

**Exit criterion:** repeatable web capture with evidence IDs and no global REA reconfiguration.

---

# Phase 1 — Repository foundation

Create only the minimum durable structure needed for forensic work:

```text
docs/
  architecture/
  methodology/
  lab/
schemas/
forensics/
  vendors/
  upstreams/
evidence/
  manifests/
experiments/
collector_specs/
src/
tests/
```

Large/raw captures should not be blindly committed to Git. Store manifests, hashes, metadata, and reproducible references; decide separately which raw artifacts belong in object storage, WARC storage, or Git LFS.

Core schemas to create:

1. `SourceMap`
2. `VendorDecomposition`
3. `Claim`
4. `EvidenceRef`
5. `CollectorSpec`
6. `SourceDriftEvent`
7. `ValidationResult`

**Exit criterion:** schemas can represent a real FastMoss field from UI/API through upstream hypothesis and validation result.

---

# Phase 2 — FastMoss reconnaissance

Do not attempt to map the whole product in one session.

Split FastMoss into surfaces:

1. product discovery/ranking;
2. product detail/history;
3. shops;
4. creators;
5. videos;
6. LIVE;
7. categories/market;
8. exports;
9. official API;
10. MCP.

For each surface, use one or more bounded REA work units.

## Standard REA work unit

Each unit investigates one user action or one question only.

Example:

> What backend contract powers `Product Search -> Brazil -> Beauty -> 7 days -> GMV descending`?

Capture:
- starting URL/state;
- action sequence;
- JS chunks involved;
- endpoint/operation candidates;
- request shape;
- response shape;
- IDs and enums;
- pagination;
- timestamps;
- client-side transformations;
- evidence references;
- unknowns.

Artifacts:

```text
forensics/vendors/fastmoss/<surface>/
  README.md
  observations/
  endpoint-candidates/
  field-map.yaml
  claims.yaml
  evidence-manifest.yaml
```

**Stop condition for every work unit:** one question answered with evidence, or explicitly marked unknown. Never expand scope mid-session.

---

# Phase 3 — FastMoss backend-contract reconstruction

Merge individual observations into a coherent vendor model:

```text
Provider
 -> Surface
 -> Feature
 -> Request/Operation
 -> Entity
 -> Field
 -> MetricDefinition
 -> Relationship
 -> VendorClaim
 -> Evidence
```

Explicitly identify:
- canonical IDs;
- alternate IDs;
- region/category enums;
- temporal-window semantics;
- cursor/page semantics;
- stable vs ephemeral fields;
- client joins;
- likely server joins;
- fields apparently raw vs derived vs modeled;
- cache/freshness behavior;
- source drift.

Deliverable:
- `forensics/vendors/fastmoss/VENDOR_DECOMPOSITION.yaml`

---

# Phase 4 — Upstream attribution

For every high-value FastMoss field, search for the most primary sustainable source.

Priority:

```text
official public API
 -> official authorized API
 -> official public surface
 -> public structured endpoint
 -> deterministic HTTP collection
 -> deterministic browser collection
 -> licensed third-party source
 -> historical derivation
 -> statistical model
```

Example field study:

```text
FastMoss day7_units_sold
 -> identify field semantics
 -> identify TikTok primitive(s)
 -> observe cumulative sold count over time
 -> test rolling-window derivation
 -> quantify disagreement
```

Deliverables:
- `forensics/upstreams/tiktok-shop/SOURCE_MAP.yaml`
- one `CollectorSpec` per approved primitive.

---

# Phase 5 — Independent TikTok data plane

Only after upstream attribution is evidenced, implement collectors.

Separate:

### Discovery collectors
Find new products, shops, creators, videos, ads, LIVE sessions, and relationships.

### Refresh collectors
Revisit known entities at adaptive frequencies.

### Event collectors
Capture short-lived/high-value events where applicable.

### Snapshot collectors
Append longitudinal observations; never overwrite prior state.

Escalation ladder:

```text
L0 official API
L1 structured HTTP
L2 raw HTTP extraction
L3 HTTP + authorized session
L4 deterministic browser
L5 browser + network instrumentation
L6 semantic/agentic browser only when required
```

REA leaves the hot path once a stable CollectorSpec exists.

---

# Phase 6 — PiPiADS, Minea, Kalodata

Repeat the same method, but do not duplicate solved primitives.

## PiPiADS focus

- ad identity;
- advertiser identity;
- creative identity;
- first/last seen;
- landing URLs;
- geography;
- engagement;
- spend/conversion/order estimates;
- store/product linkage.

## Minea focus

- cross-platform entity joins;
- Meta/TikTok/Pinterest coverage;
- store/product/creative relationships;
- historical discovery;
- ranking/trending logic.

## Kalodata focus

- direct field-by-field comparison with FastMoss;
- API contract differences;
- historical-window semantics;
- revenue/GMV estimation differences;
- creator/product/video/LIVE graph differences;
- disagreement as a clue to modeled vs direct metrics.

Output for each vendor:
- decomposition graph;
- upstream map;
- reproduction matrix;
- unique capability list;
- redundant capability list.

---

# Phase 7 — Cross-vendor forensic comparison

Create a canonical ontology independent of vendor naming:

```text
Product
Shop/Seller
Creator
Video
AdCreative
Advertiser
Livestream
Category
Offer
PriceObservation
SalesObservation
RankObservation
RelationshipObservation
```

Then map vendor fields onto canonical metrics.

For every disputed metric retain:
- exact vendor definition if documented;
- observed behavior;
- inferred definition;
- confidence;
- vendor-vendor disagreement;
- vendor-upstream disagreement;
- our reconstruction error.

This is where R/Python validation becomes central.

---

# Phase 8 — Data architecture and science

Candidate architecture to benchmark:

```text
RAW immutable evidence
 -> append-only OBSERVATIONS
 -> canonical ENTITY GRAPH
 -> DERIVED features
 -> versioned MODELS
 -> query/index layer
 -> alerts/API/MCP/UI
```

Benchmark locally before standardizing:
- Parquet + DuckDB;
- Arrow datasets;
- Polars/Parquet;
- add ClickHouse only when scale/serving requirements justify it.

Statistical work:
- missingness;
- bias;
- source disagreement;
- rolling deltas;
- velocity/acceleration;
- change points;
- anomaly detection;
- model calibration;
- uncertainty intervals;
- temporal leakage controls.

---

# Phase 9 — Expand beyond TikTok

After TikTok architecture proves itself, add source families, not random websites.

Suggested sequence:

1. Amazon / Keepa / seller-intelligence vendors;
2. Meta Ads / Google Ads transparency;
3. Shopify public storefront graph;
4. Shopee;
5. AliExpress / Alibaba ecosystem;
6. Temu;
7. Google Shopping/Search;
8. YouTube/Instagram/Pinterest commerce signals;
9. country-specific marketplaces.

Every new family starts with `Source Forensics`, not with a production scraper.

---

# Desktop Commander session discipline

To avoid oversized sessions, every implementation session follows this contract:

1. **One explicit question.**
2. **One target/surface.**
3. **One bounded capture or implementation change.**
4. **One verification step.**
5. **One durable artifact/commit.**
6. **One short session report:** found / unknown / next question.

Never combine in one Desktop Commander unit:
- two vendors;
- broad reconnaissance plus production collector implementation;
- REA/Nix infrastructure repair plus vendor analysis;
- schema redesign plus large captures;
- multiple unrelated source families.

This allows interruption/resumption without losing forensic state.

---

# Immediate execution sequence

1. Record REA/Nix baseline.
2. Validate REA web lane against a disposable browser.
3. Create canonical schemas.
4. Run first FastMoss public-surface capture.
5. Map Product Search.
6. Map Product Detail/history.
7. Map Shop.
8. Map Creator.
9. Map Video/LIVE.
10. Reconstruct FastMoss entity/endpoint graph.
11. Perform upstream attribution for the first 10 high-value fields.
12. Build the first TikTok CollectorSpecs.
13. Implement the smallest independent longitudinal collector.
14. Validate our observations against FastMoss.
15. Start PiPiADS.
16. Start Minea.
17. Start Kalodata.
18. Build cross-vendor canonical ontology and disagreement analysis.

## First technical success criterion

Source Forensics can take one commercially meaningful FastMoss metric and produce a fully evidenced chain:

```text
FastMoss feature
 -> observable backend field
 -> semantic definition
 -> upstream primitive(s)
 -> our acquisition method
 -> historical/derived/model logic
 -> our reproduced value
 -> error/cost/freshness/confidence
```

Only after this succeeds should the project scale horizontally across hundreds of fields and additional marketplaces.
