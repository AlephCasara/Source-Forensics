# Source Forensics — Hourly Execution Roadmap

## Purpose

This document decomposes the project into bounded work blocks designed to fit within one ChatGPT/Desktop Commander execution window. One scheduled run executes **one block only**, produces durable evidence/code/docs, updates `docs/execution/STATE.md`, commits coherent work, and stops. The next scheduled run resumes from that state.

This is an execution plan, not a promise that every block will consume exactly 60 minutes. A block is deliberately scoped so it can finish safely inside the available window. If a block finishes early, use the remaining time for verification, documentation and cleanup — **do not start the next block**.

## Mandatory execution contract

Every hourly run must:

1. Read `docs/execution/STATE.md`, this roadmap, `ROADMAP.md`, and any artifact referenced by `current_block`.
2. Confirm repository/local state before modifying anything.
3. Work on exactly one `current_block`.
4. Use Desktop Commander only for that block's local inspection/execution.
5. Use GitHub for durable repository state; do not leave important findings only in chat or terminal output.
6. Preserve raw evidence outside Git when large/sensitive, but commit manifests/hashes/analysis needed to reproduce conclusions.
7. End with verification or an explicit `BLOCKED` result.
8. Update `STATE.md` with `FOUND / UNKNOWN / EVIDENCE / DECISION / NEXT`.
9. Commit/push coherent artifacts when appropriate.
10. Stop. Never roll directly into the next block in the same run.

If a block cannot finish safely, split it in `STATE.md` as `Hxx-A`, `Hxx-B` rather than expanding scope.

## Tool roles

- **REA 6.5.0**: web/application reverse engineering, evidence, JS/runtime reconciliation, binary/artifact analysis where applicable.
- **Chromium/CDP**: controlled and passive browser observation.
- **mitmproxy / HAR**: retained network evidence and offline inspection.
- **Ghidra / JADX / ILSpy / native RE tools**: use only if a relevant vendor distributes native/mobile artifacts worth analyzing; never force binary analysis onto a web-only question.
- **HTTP/crawling stack** (`httpx`, `curl_cffi`, Scrapling, Crawlee, Scrapy): reproduction candidates after a contract is understood.
- **Browser stack** (Playwright/Patchright/Camoufox/etc.): escalation candidates for collectors, not default forensic substitutes for REA.
- **DuckDB/Arrow/Parquet/Polars/R/Python**: data validation, temporal history, derivations, models and benchmarking.
- **GitHub**: durable source of truth for architecture, state, evidence manifests, schemas, code and ADRs.
- **Desktop Commander**: local execution/inspection; each scheduled run uses a bounded subset of its capabilities.

## Scope discipline

Never combine two vendors in one block. Never mix REA/Nix infrastructure repair with vendor reverse engineering. Never mix broad reconnaissance with production collector implementation. Never silently broaden a question after new evidence appears; record the new question in `STATE.md` for a future block.

---

# PHASE 1 — Trustworthy forensic laboratory

### H01 — Recover and normalize current Phase 1 state
Inspect active/stale local processes from the interrupted smoke test, verify fixture/repo artifacts, record what was already completed, safely terminate only disposable forensic processes if appropriate, and establish a clean repeatable baseline.

**Exit:** exact Phase 1 state is known and documented; no ambiguous stale processes.

### H02 — Controlled browser capture validation
Re-run or verify the controlled fixture scenario: click -> JS listener -> fetch -> JSON -> DOM update. Confirm request/response content capture and deterministic reproduction.

**Exit:** active scenario evidence proves end-to-end controlled capture.

### H03 — Passive causality / listener attribution
Use separate passive observation against the fixture. Verify listener location and request initiator/source attribution without overlapping active capture on the same target.

**Exit:** causal chain from action to shipped script/source location is evidenced, or the exact missing REA capability is documented.

### H04 — Execution, script export and source-map reconciliation
Test focused execution coverage, export captured scripts, run static JS application analysis, recover readable sources/modules as useful, and trace a generated location through the source map.

**Exit:** runtime evidence can be reconciled to static/script/source-map evidence by identity/digest.

### H05 — Retained network evidence path
Generate a HAR and/or mitmproxy capture for the fixture and validate REA offline `inspect-web-network-capture` behavior. Document where network evidence is richer/weaker than browser-scenario evidence.

**Exit:** offline transaction evidence is reproducibly inspectable.

### H06 — Differential capture and evidence-integrity checks
Run baseline vs one-variable-changed fixture captures. Test `compare-web-captures`, independently verify source/artifact digests, and document REA 6.5.0 comparison limitations/workarounds.

**Exit:** comparison methodology cannot silently mistake changed artifacts for equality.

### H07 — Evidence schema + reproducibility harness
Create/finish experiment manifest schema and a small repeatable harness or documented command sequence for fixture runs. Ensure raw evidence paths, hashes, versions, question, limitations and confidence are recorded.

**Exit:** another agent/chat can reproduce the smoke experiment from the repository.

### H08 — Phase 1 gate
Review all Phase 1 evidence. Decide the production forensic workflow: REA-only where reliable, REA+CDP/HAR/mitmproxy where needed. Create ADR and update methodology.

**Exit:** explicit GO/GO-WITH-CONSTRAINTS/NO-GO for REA web forensics on this NixOS host.

---

# PHASE 2 — Vendor reverse engineering

## FastMoss

### H09 — FastMoss surface inventory and experiment matrix
Map public/authorized surfaces and translate them into bounded forensic questions. Do not deeply capture yet.

### H10 — FastMoss Product Search: controlled capture
One representative Product Search interaction, including Brazil/region/filter/sort if available legitimately.

### H11 — FastMoss Product Search: passive/static reconciliation
Listener/initiator, relevant bundle/module, request construction, response schema and source-map/static evidence.

### H12 — FastMoss Product Detail
Entity IDs, seller/product relationships, primary facts, request/response contracts.

### H13 — FastMoss Product History / temporal semantics
Historical chart/window requests, timestamp meanings, cumulative vs rolling metrics, visible derivations.

### H14 — FastMoss Shops
Shop identity, product/shop graph, ranking/sales fields, pagination/filter contracts.

### H15 — FastMoss Creators
Creator identity, creator-product relationships, GMV/sales/engagement fields, temporal windows.

### H16 — FastMoss Shoppable Videos
Video identity, product/creator links, visible sales/GMV/engagement relationships.

### H17 — FastMoss LIVE
Livestream identity, shop/creator/product relations and transient/temporal behavior.

### H18 — FastMoss Categories / rankings / market views
Category IDs, region enums, ranking windows, sorting and aggregation contracts.

### H19 — FastMoss exports
Export job/request semantics, exported schema and differences from UI representation.

### H20 — FastMoss official API contract comparison
Compare documented API entities/fields/semantics against observed web-client contracts. Record aliases and discrepancies.

### H21 — FastMoss MCP contract
Map exposed MCP tools/resources against web/API capabilities; identify unique semantic abstractions vs thin wrappers.

### H22 — FastMoss entity/identity graph
Consolidate canonical/alternate IDs and relationships across Product, Shop, Creator, Video, LIVE and Category.

### H23 — FastMoss field and metric semantics
Classify important fields by observation/transformation/temporal/source-authority axes; identify opaque server-side/modelled metrics.

### H24 — FastMoss decomposition gate
Produce FastMoss `VendorDecomposition`, unknowns, likely upstream hypotheses, feature-creep/redesign assessment and Phase 3 candidates.

## PiPiADS

### H25 — PiPiADS surface inventory
Bounded experiment matrix for ads, advertisers, creatives, landing pages, products/stores and estimates.

### H26 — PiPiADS ad discovery contract
Capture search/filter/pagination/ad identity and first/last seen semantics.

### H27 — PiPiADS creative + advertiser graph
Creative identity, advertiser identity, engagement/geography and relationships.

### H28 — PiPiADS landing/store/product linkage
Trace cross-domain/entity relationships exposed to the client.

### H29 — PiPiADS modeled metrics
Black-box study of estimated spend/conversions/orders: inputs visible to client, temporal behavior, sensitivity tests where feasible.

### H30 — PiPiADS static/runtime consolidation
Bundle/source/endpoint/entity reconciliation and evidence gap closure.

### H31 — PiPiADS decomposition gate
Vendor decomposition, unique/redundant capabilities, upstream/model hypotheses and redesign classification.

## Minea

### H32 — Minea surface inventory
Experiment matrix for Meta/TikTok/Pinterest ads, products, stores and discovery.

### H33 — Minea ad/search contract
Identity, filtering, pagination, history, platform semantics.

### H34 — Minea store/product graph
Landing/store/product/entity links and ecommerce-platform attribution.

### H35 — Minea cross-platform relations
How client representation links creatives/products/advertisers across platforms.

### H36 — Minea ranking/trending/history
Visible ranking/window/history logic and derived/modelled candidates.

### H37 — Minea static/runtime consolidation
Endpoint/module/entity graph and targeted evidence gap closure.

### H38 — Minea decomposition gate
Vendor decomposition, unique/redundant capabilities, hypotheses and redesign classification.

## Kalodata

### H39 — Kalodata inventory + comparator matrix
Choose fields/features that directly arbitrate FastMoss claims.

### H40 — Kalodata product/search contracts
Product/search/request/schema/temporal semantics.

### H41 — Kalodata creator/video/LIVE graph
Identity/relationships and visible metrics.

### H42 — Kalodata API/web disagreement study
Compare documented API with web client and FastMoss for representative entities/metrics.

### H43 — Kalodata decomposition gate
Vendor decomposition and disagreement hypotheses.

## Cross-vendor synthesis

### H44 — Canonical ontology v1
Map vendor-specific entities/fields to vendor-independent canonical entities/observations/claims/metrics.

### H45 — Metric disagreement matrix
Compare definitions/values for representative shared metrics and classify causes: source, window, derivation, model, lag, unknown.

### H46 — Phase 2 gate
Prioritize high-value capabilities for upstream attribution. Drop feature creep and low-value parity work.

---

# PHASE 3 — Upstream attribution and reproduction

### H47 — TikTok source/access matrix
Official APIs, authorized APIs, public surfaces, geographic/rights constraints, structured endpoints and candidate primitives.

### H48 — TikTok product primitives
Product identity, price, sold/review/category/shop primitives and coverage.

### H49 — TikTok shop/seller primitives
Shop identity, product graph, seller metrics and availability.

### H50 — TikTok creator/video/LIVE primitives
Creator/video/LIVE relationships and directly observable facts.

### H51 — TikTok advertising primitives
Creative/advertiser/transparency/Creative Center surfaces and coverage limits.

### H52 — Longitudinal snapshot experiment
Collect a small representative cohort using the cheapest viable acquisition method; define grain and temporal fields correctly.

### H53 — Historical derivation experiment
Test at least one rolling/delta metric (for example 7-day sold units) from our own snapshots.

### H54 — Cross-vendor validation
Compare our primitive/derived values against FastMoss/Kalodata/PiPiADS/Minea where semantically comparable.

### H55 — CollectorSpecs v1
Write CollectorSpecs for approved TikTok primitives, including primary/fallback acquisition and provenance requirements.

### H56 — Cost/reliability/maintenance benchmark
Estimate or measure marginal cost, browser dependency, failure modes, refresh burden and expected drift.

### H57 — Reproduction matrix
Capability-by-capability `REPLACE / AUGMENT / BUY / DROP / MODEL` candidate decisions with confidence.

### H58 — Phase 3 gate
Choose exactly which capabilities are rational to implement in the local engine.

---

# PHASE 4 — Native local engine

### H59 — Architecture ADRs and package boundaries
Finalize bounded contexts, storage/control-plane choices and minimal implementation architecture.

### H60 — Canonical schemas
Implement core Source, Entity, ExternalIdentity, Observation, Claim, EvidenceRef, MetricDefinition, ValidationResult structures.

### H61 — Raw/evidence storage layer
Content-addressed/raw artifact convention, manifests, hashes and retention rules.

### H62 — Observation storage layer
Append-only observations with explicit grain and temporal semantics; benchmark Parquet/Arrow/DuckDB path.

### H63 — Entity resolution/identity layer
Initial TikTok entity graph and external-ID mapping.

### H64 — Collector runtime skeleton
Implement one approved primitive collector from CollectorSpec with deterministic retries/errors/provenance.

### H65 — Snapshot/refresh control plane
Checkpointing, scheduling semantics, refresh policy and failure state without overengineering.

### H66 — Derived metric engine
Reproducible derivations from observations; version formulas and semantics.

### H67 — R/Python validation layer
Provider reproduction validation, missingness, error, bias, temporal analysis and uncertainty.

### H68 — Semantic/query layer
Canonical metrics/dimensions and one simple local query interface; no dashboard feature creep.

### H69 — Minimal agent interface
Expose a small MCP/API or equivalent intent-oriented interface that can answer one useful market-intelligence question.

### H70 — Phase 4 benchmark gate
Test end-to-end utility, cost, freshness, correctness and operational burden against vendor workflow.

---

# PHASE 5 — Expansion and final replacement strategy

### H71 — Expansion economics and source-family ranking
Rank next families by internal utility, data accessibility, cost and strategic value.

### H72 — Amazon/Keepa specimen inventory
Map the Amazon historical/competitive-intelligence archetype.

### H73 — Amazon upstream/source matrix
Official seller/catalog APIs vs public competitive surfaces and their access boundaries.

### H74 — Keepa reverse-engineering study
One bounded high-value capability end to end.

### H75 — Amazon comparator study
Jungle Scout or Helium 10 only where needed to arbitrate/learn a distinct capability.

### H76 — Amazon reproduction decision
Collector/derivation feasibility and `REPLACE/AUGMENT/BUY/DROP/MODEL` decisions.

### H77 — Meta family pilot
One bounded ad/market-intelligence capability and its upstream path.

### H78 — Google family pilot
One bounded ads/shopping/search intelligence capability.

### H79 — Shopify ecosystem pilot
Public storefront intelligence vs authorized merchant data; entity/store/product graph.

### H80 — Shopee pilot
One high-value capability and access/reproduction feasibility.

### H81 — AliExpress/Alibaba/Temu pilot
Supplier/product intelligence primitives and cross-market linkage feasibility.

### H82 — Cross-market semantic alignment
Extend canonical ontology without leaking vendor/platform schemas into the core.

### H83 — Global data-quality and operational benchmark
Freshness, drift, coverage, cost, missingness and reliability across implemented families.

### H84 — Replacement matrix
Final capability-level `REPLACE / AUGMENT / BUY / DROP / MODEL` matrix for the current scope.

### H85 — Interaction/data-design compression pass
Reduce exposed controls to user intents; identify internal complexity that should never become UI. Apply KEEP/COMPRESS/INTERNALIZE/DROP decisions.

### H86 — Project gate
Assess whether Source Forensics is demonstrably better for our local use. Document next build horizon, rational paid dependencies and features intentionally not built.

---

## After H86

Do not invent more features automatically. Use the evidence and replacement matrix to create the next bounded roadmap only for capabilities that proved useful. Expansion remains source-family-by-source-family and continues under the same one-block-per-hour execution contract.
