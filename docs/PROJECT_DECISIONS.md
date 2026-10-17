# Source Forensics — Project Decisions

This file records the major decisions made before Phase 1 so they are not lost in chat history and can be treated as project constraints until explicitly superseded by an ADR.

## 1. Primary objective

Source Forensics exists first to determine whether we can build a better, cheaper, local-first market-intelligence system than the useful parts of FastMoss, PiPiADS, Minea and comparable vendors.

The first customer is our own workstation and workflows. Commercialization is optional and must not distort the initial architecture.

## 2. No feature cloning

We do not want a clone with the same number of screens, filters or buttons.

The design goal is semantic compression: reduce many vendor features into the smallest coherent set of user intents, domain concepts, primitives and signals that explain the real work.

A vendor feature can be classified as:

- KEEP — intrinsically useful as exposed;
- COMPRESS — several vendor interactions should become one higher-level intent;
- INTERNALIZE — useful logic should exist but remain invisible to the user;
- REPLACE — our implementation should supersede it;
- DROP — feature creep or low-value capability;
- BUY — vendor remains economically/technically superior;
- MODEL — no direct primitive exists, but an explicit estimate can be useful.

## 3. Reverse engineering is evidence-driven

REA 6.5.0 is the primary reconnaissance/evidence tool for web reverse engineering, supplemented by CDP, HAR, mitmproxy and other retained artifacts when needed.

The workflow is:

question -> hypothesis -> controlled experiment -> raw evidence -> static/runtime analysis -> differential comparison -> conclusion + confidence.

Active scenarios and passive observation should be separated. Static analysis must not be presented as proof of runtime behavior. REA summaries are not treated as ground truth when underlying artifacts can be independently verified.

## 4. Initial vendor specimens

Order of initial investigation:

1. FastMoss — first complete specimen for TikTok commerce intelligence;
2. PiPiADS — ad intelligence, historical observation and modeled metrics;
3. Minea — cross-platform ad/product/store relationships;
4. Kalodata — independent comparator for TikTok commerce fields, semantics and disagreement analysis.

Other vendors are added only when they answer a specific unresolved forensic question or represent a materially different source archetype.

## 5. Vendor schemas remain at the edge

FastMoss/PiPiADS/Minea/Kalodata schemas must not become the canonical Source Forensics domain model.

Vendor representations are adapters, claims and evidence.

The canonical model will be built around concepts such as:

- Source;
- Entity;
- ExternalIdentity;
- Relationship;
- Observation;
- Claim;
- EvidenceRef;
- AcquisitionRun;
- MetricDefinition;
- DerivedMetric;
- ModelEstimate;
- Signal;
- ValidationResult.

## 6. Grain must be explicit

Every fact/observation type must declare what one record means before schema design proceeds.

Examples that must remain conceptually distinct:

- a product entity;
- a price observed at a point in time;
- a cumulative sold counter;
- a vendor's 7-day GMV claim;
- our derived 7-day GMV;
- our model estimate with uncertainty.

A dashboard may show them together; the data model must not pretend they are the same kind of fact.

## 7. Time is first-class

Where applicable we distinguish:

- source/event time;
- valid time;
- observed time;
- ingestion time;
- processing time;
- vendor-defined analytical windows.

Bitemporal reasoning is allowed/expected when we need to distinguish when a fact was true from when Source Forensics learned it.

Historical observations are append-only whenever feasible. Do not overwrite prior state merely because a new state was observed.

## 8. Provenance and lineage are product features

Important conclusions must be traceable:

signal -> model/formula -> metric -> observations -> acquisition run -> source -> raw evidence.

The system should eventually be able to explain not only *what* it concluded but *why*, from which sources, at what time, and with what uncertainty.

## 9. Semantic layer

Metrics such as GMV, sales, growth, engagement, velocity and conversion must have canonical definitions independent of vendor naming.

A MetricDefinition should eventually capture grain, units/currency, temporal semantics, required dimensions, formula/model, primitive dependencies, caveats, provenance requirements and validation history.

UI, API, MCP, R, Python and agents should consume the same semantic definitions rather than reimplementing metrics independently.

## 10. Data architecture direction

The candidate logical stack is:

RAW immutable evidence
-> append-only OBSERVATIONS
-> canonical ENTITY/IDENTITY graph
-> DERIVED features
-> versioned MODELS
-> SIGNALS
-> delivery surfaces (local UI / API / MCP / agents).

Parquet + Arrow + DuckDB are strong candidates for the local analytical layer, but no storage/compute stack is considered final until benchmarked against realistic workloads.

Control-plane concerns (jobs, retries, checkpoints, collector status, versions, leases) should remain conceptually separate from analytical storage.

## 11. Acquisition strategy

For each primitive, use the most primary sustainable source that satisfies the requirement.

General escalation order:

1. official public API;
2. official authorized API;
3. official public surface;
4. public structured endpoint;
5. deterministic HTTP collection;
6. authorized-session collection where appropriate;
7. deterministic browser;
8. browser/network instrumentation;
9. semantic/agentic browser only when simpler approaches fail;
10. licensed/paid third party if economically superior.

REA leaves the production hot path once a stable CollectorSpec exists.

## 12. Economic decisions are explicit

Reverse engineering is not an ideological commitment to self-host everything.

For each capability we compare:

- reproducibility;
- accuracy;
- freshness;
- failure rate;
- marginal cost;
- implementation cost;
- maintenance burden;
- vendor price;
- strategic value of owning the history/data.

Valid outcomes include REPLACE, AUGMENT, BUY, DROP and MODEL.

## 13. Source Forensics should eventually outperform vendor dashboards through cross-source intelligence

The long-term advantage is not more scraping and not more buttons.

The desired moat is:

- historical depth;
- continuous observation;
- canonical entity/identity graph;
- cross-platform joins;
- field provenance;
- semantic consistency;
- calibrated models;
- drift recovery;
- low marginal cost;
- transparent uncertainty;
- high-level signals that compress many primitives into useful decisions.

Example target behavior: explain an emerging product opportunity using simultaneous changes in commerce sales, creator activity, ads, storefront adoption, supplier pricing and search/social interest rather than exposing those sources as unrelated dashboards.

## 14. Software architecture matters as much as data architecture

Initial bounded contexts are conceptual, not necessarily separate services:

- FORENSICS — evidence, hypotheses, experiments;
- ACQUISITION — collectors, scheduling, retries;
- CANONICAL DATA — entities, identities, observations;
- SEMANTICS — metrics, dimensions, units;
- INTELLIGENCE — features, models, signals;
- DELIVERY — local UI, API, MCP, agents;
- GOVERNANCE — provenance, rights, access policy.

Do not introduce microservices merely because bounded contexts exist.

## 15. Quality and observability

A collector or model is not considered good merely because it returns a value.

We care about correctness, reliability, testability, maintainability, performance, observability, portability and recoverability.

Data-quality expectations should become executable contracts where practical: schema, nullability, ranges, freshness, units, uniqueness, provenance and retention.

Operational observability and data observability must connect so a source/schema failure can be traced to downstream metrics/signals affected by it.

## 16. Interaction design principle

The interface should model user intentions, not database tables or vendor navigation trees.

Complexity should be progressively disclosed. Advanced controls remain available but should not dominate the main workflow.

The ideal UX is closer to:

> find emerging products in Brazil and explain the evidence

than to reproducing hundreds of vendor filters and screens.

## 17. Evidence storage

Large raw artifacts (HAR/WARC/HTML/JSON/screenshots/browser profiles/databases) should not be blindly committed to Git.

Git should retain compact durable knowledge: manifests, hashes, experiment metadata, schemas, scripts, analyses, reproduction instructions and ADRs.

Raw evidence belongs in dedicated local/object storage unless a small artifact is specifically useful in-version.

## 18. Session discipline

Desktop Commander sessions must be bounded and resumable.

Default unit:

1. one explicit question;
2. one target/surface;
3. one bounded capture or implementation change;
4. one verification step;
5. one durable artifact/commit;
6. one short report: found / unknown / next question.

Do not combine vendor reconnaissance, Nix/REA infrastructure repair, production collector implementation and schema redesign into one oversized session.

## 19. Five phases

1. Forensic laboratory and trustworthy evidence.
2. Vendor reverse engineering and observable backend reconstruction.
3. Upstream attribution and reproduction study.
4. Local Source Forensics data/intelligence product.
5. Expansion across source families and replace/augment/buy/drop/model decisions.

## 20. Current status

Preparation is complete for Phase 1.

The next operational task is to validate a disposable forensic Chromium + REA web-analysis workflow on a harmless target before any real FastMoss capture.

Any future decision that changes one of the constraints above should be recorded as an ADR rather than silently changing the architecture.