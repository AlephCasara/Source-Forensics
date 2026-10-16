# Source Forensics — Engineering and Design Doctrine

## Purpose

Source Forensics exists to determine whether a local system can replace or outperform the useful capabilities of FastMoss, PiPiADS, Minea and comparable market-intelligence products without reproducing their feature creep.

The goal is not interface parity. The goal is semantic compression: understand the underlying jobs, data, decisions and evidence well enough that many vendor controls can collapse into a small number of powerful user intents.

A successful Source Forensics product should hide accidental complexity while preserving analytical depth, provenance, uncertainty and inspectability.

## Core design thesis

A vendor UI is not the domain model.

A vendor endpoint is not the data model.

A vendor metric name is not a semantic definition.

A dashboard is not intelligence.

We will reverse engineer vendors to discover capabilities, contracts, entities, workflows, acquisition strategies and modeling assumptions. We will then redesign those findings around our own canonical domain and our own user needs.

The system should become simpler as our understanding increases.

## Disciplines treated as first-class engineering inputs

Source Forensics combines:

1. software reverse engineering and software archaeology;
2. black-box experimental analysis;
3. data architecture;
4. data engineering;
5. conceptual, logical and physical data modeling;
6. temporal data modeling;
7. semantic modeling and metric design;
8. metadata, provenance and lineage;
9. entity resolution and knowledge-graph design;
10. data quality and data observability;
11. statistical measurement, calibration and uncertainty;
12. software architecture and domain modeling;
13. information architecture;
14. interaction and service design;
15. reliability, performance and maintainability engineering;
16. security, rights and compliance engineering.

No single discipline gets to dictate the system.

---

# 1. Reverse-engineering doctrine

REA and related tools are evidence instruments, not truth machines.

Every reverse-engineering conclusion must be classified as:

- OBSERVED — directly supported by retained evidence;
- DERIVED — mechanically computed from observed evidence;
- INFERRED — analyst/model conclusion from incomplete evidence;
- UNKNOWN — insufficient evidence;
- UNAVAILABLE — outside the authority or capability of the current method.

For binaries, decompiler output is pseudocode unless exact source recovery is independently established. For web applications, static bundle analysis does not prove runtime execution. Runtime observation does not prove unobserved server implementation.

Every investigation starts from a narrow analyst question and follows the smallest evidence path capable of answering it.

Preferred order:

1. identify exact artifact/target/version;
2. establish baseline state;
3. inspect the smallest useful static surface;
4. execute a controlled differential experiment when behavior matters;
5. capture passive runtime evidence separately when attribution matters;
6. correlate runtime with shipped artifacts;
7. corroborate consequential claims using a second evidence type or tool where practical;
8. record residual unknowns.

Negative findings are bounded. “Not observed in this capture” never becomes “does not exist.”

---

# 2. Semantic compression over feature parity

We do not count vendor features as requirements.

For every vendor feature, ask:

1. What user decision or job is this feature serving?
2. What information is actually required for that decision?
3. Which primitives produce that information?
4. Can multiple vendor features be represented by one canonical operation?
5. Can the system infer intent instead of forcing the user through configuration screens?
6. What advanced controls must remain available for inspection or override?

The preferred interaction pattern is:

```text
USER INTENT
   -> semantic interpretation
   -> canonical query/analysis plan
   -> source selection
   -> evidence + computation
   -> decision-oriented result
   -> optional drill-down
```

The default surface should expose common decisions, not internal machinery.

Advanced mechanics should use progressive disclosure: visible when needed, absent when they merely create cognitive load.

“One button” is a metaphor for a coherent task model, not a requirement for a literal single-button UI.

---

# 3. Canonical data model before vendor schemas

Vendor schemas are adapter inputs. They must not become our core model.

Canonical concepts should include at least:

- Source — a platform, vendor, document, API or observable surface;
- Entity — stable conceptual object such as Product, Shop, Seller, Creator, Advertiser or Creative;
- ExternalIdentity — source-specific identifier for an Entity;
- Relationship — typed edge between entities with temporal validity and provenance;
- Observation — atomic measurement captured from a source at a known time;
- Claim — assertion made by a source or model about an entity/relationship/metric;
- EvidenceRef — immutable pointer/hash describing why an observation or claim is believed;
- AcquisitionRun — one execution that attempted to obtain observations;
- MetricDefinition — canonical semantic definition of a measurable quantity;
- DerivedMetric — deterministic computation from observations or other metrics;
- ModelEstimate — model-produced value carrying model version and uncertainty;
- Signal — decision-oriented interpretation built from metrics/relationships/models;
- ValidationResult — comparison against another source, observation or later outcome.

The model must keep these distinct. A vendor claim is not an observation. An estimate is not a direct measurement. A current entity attribute is not historical state.

## Declare the grain

Before creating any observational/fact structure, state exactly what one row/object represents.

Examples:

- one observation of one product price in one source at one observation time;
- one observed product-to-creator relationship in one source during one capture;
- one vendor claim about 7-day units for one product at one vendor timestamp;
- one ad creative observed in one country at one capture time.

Do not mix grains because two values are convenient to display together.

Atomic observations should be preserved even when the common user query is aggregated. Aggregations are reproducible views; lost atomicity is usually not recoverable.

---

# 4. Time is a core dimension, not a timestamp column

Market intelligence is fundamentally longitudinal.

For every temporal fact distinguish, when applicable:

- source/event time — when the event allegedly happened at the upstream source;
- valid time — when a fact is true in the modeled world;
- observed time — when our collector observed it;
- ingested time — when our system stored it;
- processing time — when a derived/model computation ran;
- vendor-reported window — e.g. “7 days”, whose exact boundary semantics must be defined or inferred.

Where source corrections or late discoveries matter, design for bitemporal reasoning: what was true when, and what did our system know when.

Never overwrite history merely because a newer value exists.

This enables:

- point-in-time reconstruction;
- rolling deltas;
- drift analysis;
- delayed-arrival analysis;
- vendor disagreement analysis;
- prevention of look-ahead/temporal leakage in models;
- reproducible historical backtests.

---

# 5. Raw, canonical, semantic and intelligence layers

Use logical separation even if the first implementation is physically simple.

```text
RAW / EVIDENCE
   -> CANONICAL OBSERVATIONS
   -> ENTITY / RELATIONSHIP GRAPH
   -> SEMANTIC METRICS
   -> DERIVED FEATURES / MODELS
   -> SIGNALS
   -> INTERACTION / API / MCP
```

## RAW / EVIDENCE

Preserve source-near artifacts and acquisition metadata. Immutable where practical.

## CANONICAL OBSERVATIONS

Typed, append-only atomic records mapped away from vendor-specific field names.

## ENTITY / RELATIONSHIP GRAPH

Resolves multiple external identities into canonical entities and records relationship confidence/provenance.

## SEMANTIC METRICS

Central definitions for metrics such as units_sold_7d, estimated_gmv, creator_growth or ad_lifetime. Definitions include grain, unit, aggregation behavior, dimensions, temporal window and derivation.

## DERIVED / MODELS

Rebuildable features and versioned statistical/model artifacts. Never silently masquerade as raw facts.

## SIGNALS

Decision-oriented outputs such as breakout probability, acceleration, cross-platform confirmation or source disagreement.

## INTERACTION

A thin layer over the semantic model. UI/API/MCP should not each reinvent metric logic.

---

# 6. Provenance and lineage are product features

Every consequential datum should be able to answer:

- where did this come from?
- what process produced it?
- which source/version was involved?
- what transformations happened?
- which model/version contributed?
- what evidence supports it?
- when was it observed and processed?
- what confidence/limitations apply?

Adopt the spirit of W3C PROV and OpenLineage: represent entities/datasets, activities/jobs/runs and their input/output relationships explicitly rather than burying lineage in logs.

A useful derived number without lineage is a debugging liability.

A useful derived number with lineage becomes auditable, calibratable and replaceable.

---

# 7. Data contracts and executable quality

Schemas alone are insufficient.

Every stable data product/interface should eventually declare a machine-readable contract containing:

- schema and types;
- field semantics and units;
- entity/grain definition;
- required/optional fields;
- uniqueness expectations;
- accepted nullability;
- valid ranges/enums;
- freshness expectation;
- retention expectation;
- provenance requirements;
- breaking-change/versioning policy;
- redistribution/rights classification where relevant.

Quality requirements should become executable assertions whenever possible.

Useful dimensions include:

- completeness;
- validity;
- uniqueness;
- consistency;
- freshness;
- accuracy against an available reference;
- source agreement/disagreement;
- temporal continuity;
- acquisition success rate;
- schema drift rate.

Do not silently coerce malformed source data into apparent correctness. Preserve the raw input, record the normalization, and expose validation failures.

---

# 8. Semantic layer: metric definitions are code

Metrics must have canonical definitions independent of UI and vendor naming.

For every metric define:

- canonical name;
- business meaning;
- subject entity;
- grain;
- unit/currency;
- aggregation behavior;
- allowed dimensions;
- time dimension and window semantics;
- formula;
- required primitives;
- whether direct, historical, derived or modeled;
- model/version if estimated;
- known caveats;
- validation history.

A metric such as `gmv_7d` must not mean one thing in a dashboard and another thing in an MCP response.

Entities, dimensions and metrics should form a semantic graph that query planners and agents can use without reimplementing joins ad hoc.

---

# 9. Domain boundaries and software architecture

Use bounded contexts so one model does not try to mean everything everywhere.

Initial contexts:

1. Forensics — evidence, hypotheses, experiments, vendor decompositions.
2. Acquisition — collectors, schedules, retries, rate behavior and raw captures.
3. Canonical Data — entities, external identities, relationships and observations.
4. Semantics — metric definitions, dimensions, units and query planning.
5. Intelligence — derived features, models, calibration and signals.
6. Delivery — local UI, API, MCP and agent interaction.
7. Governance — rights, access class, provenance policy and redistribution constraints.

Cross-context interfaces should be explicit contracts rather than shared mutable internals.

Document architecture at useful zoom levels rather than producing diagram bureaucracy. Maintain at least system-context and container-level views; component diagrams are created only where they resolve genuine ambiguity.

Architecturally significant choices receive short ADRs containing context, decision and consequences. Decisions are superseded, not silently rewritten.

---

# 10. Software quality is measurable

Features do not trump system quality.

Every major design should be evaluated against:

- functional suitability/correctness;
- reliability and recoverability;
- performance efficiency and resource use;
- usability/interaction cost;
- security and accountability;
- compatibility/interoperability;
- maintainability/modularity/testability;
- portability, especially within our NixOS/local-first environment.

A clever collector that cannot be diagnosed after upstream drift is not high quality.

A model that produces impressive numbers but cannot identify its inputs/version is not high quality.

A one-button UI whose output cannot be challenged or inspected is not high quality.

---

# 11. Interaction and information design

Design from user jobs and decisions, not from database tables or endpoint catalogs.

The primary local user questions are expected to resemble:

- What is gaining momentum?
- Why does the system think it is gaining momentum?
- What evidence supports that conclusion?
- Is the signal confirmed across independent sources?
- What changed since the last observation?
- What deserves investigation or action now?

The interface should optimize these tasks.

Principles:

- do the hard work in the system so the interaction can remain simple;
- expose the smallest number of concepts necessary for the current task;
- progressively disclose advanced filters, source detail and model controls;
- keep terminology canonical and consistent;
- show confidence, provenance and caveats beside consequential conclusions;
- allow drill-down from signal -> metric -> observation -> evidence;
- preserve an expert path without making every user operate an expert console;
- measure successful task completion, not number of screens or features.

If the interface requires the user to understand FastMoss/PiPiADS/Minea internals, our redesign failed.

---

# 12. Observability for data and software

Operational observability and data observability must meet.

For acquisition and processing flows, capture correlated telemetry for:

- run/job identity;
- source and collector version;
- duration/latency;
- retries and failure classification;
- bytes/records collected;
- resource utilization where useful;
- schema changes;
- validation results;
- freshness lag;
- missingness anomalies;
- lineage from inputs to outputs.

Use consistent semantic names across traces, metrics, logs and events so polyglot components can be correlated.

A production collector should answer not only “did it fail?” but “which assumption/source/schema changed, which outputs are affected, and what evidence supports that diagnosis?”

---

# 13. Measurement, statistical engineering and uncertainty

Source Forensics compares sources that may each be imperfect.

Therefore do not call a vendor “ground truth” merely because it is expensive or popular.

For quantitative claims, distinguish:

- measurement;
- deterministic derivation;
- heuristic;
- statistical estimate;
- model prediction.

Validation should use appropriate techniques such as:

- repeated observations;
- controlled comparisons;
- source-vs-source disagreement matrices;
- later-outcome validation;
- bias and error distributions rather than single examples;
- confidence/uncertainty intervals where meaningful;
- calibration curves for probabilities;
- cohort/segment analysis;
- temporal leakage controls;
- explicit missing-not-at-random concerns when source visibility is selective.

A model output should carry at least model/version, feature provenance, prediction time and uncertainty/quality metadata sufficient to reproduce or challenge it.

---

# 14. Vendor analysis is also redesign analysis

For every vendor surface, capture two parallel outputs.

## Forensic output

What exists and how it appears to work:

- user job;
- interaction path;
- observable backend contract;
- entities and IDs;
- data grain;
- metric semantics;
- acquisition clues;
- historical/model requirements;
- evidence and confidence.

## Redesign output

Whether we should reproduce it at all:

- KEEP — necessary capability and good interaction concept;
- COMPRESS — valuable capability but should merge into a broader intent;
- REPLACE — capability useful, vendor implementation/interaction should be redesigned;
- INTERNALIZE — required internally but should not be a user-facing feature;
- DROP — low value, redundant or feature creep;
- BUY — economically/technically superior to source externally;
- MODEL — no direct primitive; reproduce as an explicitly modeled estimate.

This prevents reverse engineering from degenerating into cloning.

---

# 15. Data-design scorecard for every discovered capability

Before implementing a vendor capability, answer:

1. User need: what decision/job does it support?
2. Canonical entity: what thing is being described?
3. Grain: what exactly does one observation/row represent?
4. Semantics: what does each metric actually mean?
5. Time: which time dimensions apply?
6. Source authority: direct, vendor, licensed, derived, modeled?
7. Provenance: can every consequential value be traced?
8. Quality: what can be tested automatically?
9. Entity resolution: how are source-specific IDs reconciled?
10. Storage: what must be immutable vs rebuildable?
11. Query pattern: what questions must be cheap?
12. Interaction: can this capability disappear behind a higher-level intent?
13. Operational burden: collection/compute/storage/maintenance cost?
14. Drift: what upstream changes could invalidate it?
15. Rights: acquisition and redistribution classification?
16. Decision: KEEP / COMPRESS / REPLACE / INTERNALIZE / DROP / BUY / MODEL.

No production implementation begins before this scorecard is sufficiently answered for the capability.

---

# 16. Phase 1 entry conditions

Phase 1 may begin when the following are true:

- repository and evidence-storage boundaries are established;
- REA baseline and NixOS limitations are documented;
- reverse-engineering evidence states are defined;
- raw evidence is excluded from accidental public commits;
- this design doctrine is accepted as the project quality baseline;
- each Desktop Commander session is constrained to one forensic question and one durable outcome;
- vendor schemas are explicitly forbidden from becoming the canonical core by accident;
- temporal/provenance requirements are treated as core schema concerns from the first real observation;
- architectural decisions that materially constrain later work will be recorded as ADRs.

Phase 1 does not require the final database, UI, ontology or technology stack to be chosen. Premature physical architecture would violate the purpose of Phase 1.

---

# 17. Research foundations used for this doctrine

The doctrine draws primarily from these established bodies of practice:

- REA evidence workflows: observations/inferences/unknowns, authority boundaries, static/runtime reconciliation and focused investigations;
- W3C PROV: explicit provenance entities, activities and agents;
- OpenLineage: datasets, jobs/runs and extensible lineage metadata;
- Kimball dimensional modeling: business process, declared grain, dimensions and facts; atomic grain first;
- temporal database design: valid/application time versus system/transaction time;
- dbt semantic modeling: shared entities, dimensions and centrally defined metrics;
- data contracts: schema + semantics + quality + service-level expectations as executable interfaces;
- Great Expectations-style executable data assertions;
- OpenTelemetry semantic conventions for consistent operational telemetry;
- Domain-Driven Design bounded contexts for model boundaries;
- C4 for architecture communication at useful levels of abstraction;
- ISO/IEC 25010 product-quality characteristics;
- ADR practice for preserving architectural rationale;
- progressive disclosure and service-design guidance: start from user needs, do less, and make complex systems simple to operate;
- FAIR principles where applicable to internal metadata: findability, accessibility, interoperability, reusability and provenance.

These are inputs, not dogma. Patterns are adopted only when they solve an observed Source Forensics problem.
