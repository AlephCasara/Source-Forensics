# FM-004 — FastMoss Product Detail Anatomy

## Question

For a real Brazilian product observed in FastMoss Product Search, what backend modules compose Product Detail, which identifiers connect Product -> Shop -> Creator/Video/LIVE, what is available to a public visitor, and where do detail/subscription limits begin?

## Target

```text
FastMoss product ID: 1731916815699052495
Region: BR
Shop: Semélle
Seller ID: 7496266893040520143
```

FastMoss `baseInfo` exposes the upstream TikTok Shop URL:

```text
https://shop.tiktok.com/view/product/1731916815699052495?region=BR&locale=en&source=agency
```

This URL becomes the primary anchor for the next upstream-attribution experiment.

## Status

**Answered for Product Detail composition and the visitor access boundary.**

FM-004 demonstrates that Product Detail is not one monolithic resource. It is a composition of lightweight identity, aggregate product/shop facts, relationship datasets, and higher-order analytics with different access classes.

## 1. Product Detail is modular

The visible page presents a single long detail experience, but the client decomposes it into independent capabilities:

```text
baseInfo
base aggregates
overview/history
related creators
creator charts
paid traffic / ads
related videos
related LIVE sessions
VOC
reviews
similar products
SKU / attributes
```

This is a useful design lesson for Source Forensics: a `Product` entity should not become a 200-column nullable object. Identity, observations, relationships and analytical products have different grains and lifecycles.

## 2. Access must be classified by business code, not HTTP status

Several FastMoss APIs return HTTP 200 even when the requested analytical capability is not authorized.

The shipped client maps:

```text
MAG_AUTH_3002 -> detailLimit
MAG_AUTH_3017 -> detailLimit
MSG_30001     -> login flow
```

Therefore Source Forensics uses the application-level business code as the semantic access boundary.

Examples observed:

| Capability | Endpoint | Business code | Classification |
|---|---|---:|---|
| Lightweight product identity | `/api/goods/v3/baseInfo` | `200` | public visitor |
| Product/shop aggregates | `/api/goods/v3/base` | `200` | public visitor |
| Overview/history analytics | `/api/goods/v3/overview` | `MAG_AUTH_3017` | detail limit |
| Creator list | `/api/goods/v3/author` | `200` | public visitor |
| Creator chart | `/api/goods/v3/authorChart` | `MAG_AUTH_3017` | detail limit |
| Video relations | `/api/goods/v3/video` | `200` | public visitor, default window |
| LIVE relations | `/api/goods/v3/live` | `200` | public visitor, default window |
| Paid-traffic videos | `/api/goods/V3/adsVideo` | `MAG_AUTH_3017` | detail limit |
| Paid-traffic summary | `/api/goods/V3/investment` | `MAG_AUTH_3017` | detail limit |
| Reviews | `/api/goods/reviewList` | `MAG_AUTH_3017` | detail limit |
| Similar-product analytics | `/api/goods/v3/similarity` | `MAG_AUTH_3002` | detail limit |
| User state | `/api/user/index/userInfo` | `MSG_30001` | login required |

See `artifacts/access-matrix.json` for the normalized matrix.

### Policy

When a response is marked `detailLimit`, Source Forensics may record that the capability and response schema exist, but **does not consume the restricted values as product data and does not attempt to bypass the gate**.

The FastMoss UI may still render masked/example/demo-looking content around gated sections. Such values are not treated as factual evidence for the target entity.

## 3. `baseInfo` is a lightweight identity/metadata capability

The public visitor `baseInfo` response provides product identity and relatively cheap metadata such as:

- title;
- region and region name;
- category hierarchy;
- currency;
- current displayed price;
- review count;
- product rating;
- launch time;
- upstream TikTok Shop detail URL;
- shop identity (seller ID, name, region).

For the target product it observed:

```text
region = BR
currency = BRL
current price = R$29,90
review_count = 54,805
product_rating = 4.8
seller_id = 7496266893040520143
shop = Semélle
```

### Design implication

A Source Forensics API can profit from the same pattern:

```text
ProductIdentity / ProductMetadata
```

should be independently retrievable from expensive historical analytics.

## 4. `base` adds aggregate commercial facts

The public `base` capability adds aggregate product/shop facts.

Observed product aggregates:

```text
sold_count = 403,978
sale_amount = 4,560,349.82
author_count = 16,402
aweme_count = 41,369
live_count = 0
commission_rate = 10%
```

Observed shop aggregates:

```text
shop sold_count = 411,412
shop sale_amount = 4,847,099.84
```

Cross-surface comparison with FM-003 Product Search showed exact agreement for:

- cumulative product sold count;
- creator count;
- video count;
- commission.

Product Detail retained greater GMV precision than the Product Search response used in FM-003:

```text
Search: 4,560,349
Detail: 4,560,349.82
```

This supports storing raw numeric values independently from vendor display/rounding projections.

## 5. Count fields cannot be unified by name

FM-004 found a critical grain warning.

### Creator counts

```text
Search relate_author_count = 16,402
Detail base author_count   = 16,402
Creator-list total         = 12,370
```

The creator list request has no explicit date parameter in the observed default request, so the reason for the difference remains unresolved.

### Video counts

```text
Search relate_video_count = 41,369
Detail base aweme_count    = 41,369
Video relation total      = 24,233
```

The video relation request explicitly contains:

```text
date_type=28
```

Therefore `24,233` is a 28-day relation-list total, while `41,369` is a broader count whose exact time grain remains unproven.

The UI exposes a video date filter with:

```text
7 / 28 / 90 / All
```

but attempting `All` as a visitor opens the login modal and generates no new video query. We therefore do **not** infer an all-time total by bypassing that gate.

### LIVE counts

```text
Search relate_live_count = 45,541
Detail base live_count    = 0
LIVE relation total       = 19,085
```

The LIVE relation request explicitly contains:

```text
d_type=28
```

These three facts are kept separate. `base.live_count` must not be silently mapped to `relate_live_count` merely because both names mention LIVE.

See `artifacts/relationship-semantics.json`.

## 6. Product -> Creator is a first-class relationship dataset

Public request:

```text
GET /api/goods/v3/author
```

Observed query includes:

```text
product_id=1731916815699052495
order=2,2
pagesize=5
ecommerce_type=all
```

Response fields include creator identity and commerce relationship metrics such as:

- `uid`;
- `unique_id`;
- nickname;
- product ID;
- region;
- units sold;
- GMV;
- 28-day GMV;
- video count;
- followers/categories/GPM-related fields.

This should become a canonical relationship/observation grain, not nested mutable state inside `Product`.

Candidate conceptual grain:

```text
ProductCreatorRelationshipObservation
  product_entity
  creator_entity
  observation/window semantics
  units_sold
  gmv
  content_count
  provenance
```

## 7. Product -> Video is a first-class relationship dataset

Public default request:

```text
GET /api/goods/v3/video
```

Observed defaults include:

```text
page=1
product_id=...
order=1,2
pagesize=5
is_promoted=-1
date_type=28
```

Response row fields include:

- `video_id`;
- creator IDs;
- product ID;
- seller ID;
- region;
- units sold / GMV;
- play count;
- engagement fields;
- ad flag;
- estimated ad cost;
- ROAS.

The coexistence of commerce and advertising estimates makes this an especially important future provenance study: direct engagement, attributed sales and modelled ad metrics may have different origins even within one row.

## 8. Product -> LIVE is an event/session relationship dataset

Public default request:

```text
GET /api/goods/v3/live
```

Observed defaults include:

```text
product_id=...
page=1
d_type=28
order=2,2
pagesize=5
live_type=all
```

Rows include:

- `room_id`;
- creator UID;
- product ID;
- seller ID;
- region;
- session timestamps;
- units / GMV;
- incremental units / GMV;
- audience/session metrics.

This strongly suggests a canonical event grain:

```text
LiveSession
+ ProductLiveRelationshipObservation
```

rather than a generic `live_count` column on Product.

## 9. Product Detail contains independent higher-order analytics

Static/runtime evidence reveals separate modules for:

- overview/history tables;
- creator charts;
- ad/paid traffic analysis;
- investment/paid-traffic summary;
- reviews;
- similar products;
- VOC/consumer portrait;
- SKU/attributes/translations;
- price history/list capability.

Most observed higher-order analytical modules are detail-limited for a visitor. Their existence is useful for capability decomposition even though their gated values are excluded.

This is precisely the distinction Source Forensics needs:

```text
Capability exists
!=
Capability data is public
!=
Capability must be reproduced
```

## 10. Static modules support the runtime decomposition

Key shipped-client modules observed:

### Lightweight baseInfo helper

```text
/api/goods/v3/baseInfo
/api/collect/collectStatus
```

### Shared goods-domain wrapper module

```text
/api/goods/v3/base
/api/goods/productSku
/api/goods/v3/goodsAttribute
/api/goods/v3/transAttribute
/api/goods/v3/author
/api/goods/v3/authorChart
/api/goods/v3/live
/api/goods/reviewList
/api/goods/v3/priceList
```

### Product Detail route modules

```text
/api/goods/v3/overview
/api/goods/v3/video
/api/goods/V3/adsVideo
/api/goods/V3/investment
/api/goods/v3/similarity
/api/ai/productReviewExample/getConsumerPortrait
```

### Authorization module

Maps vendor business codes to concepts including `detailLimit` and login state.

Third-party bundle bytes remain local/ignored. URLs, hashes, sizes and semantic extracts are retained in `artifacts/script-evidence.json`.

## 11. UI lazy loading is not itself causal attribution

Product Detail sections are lazy loaded as they enter the viewport. Jumping to a lower hash anchor can cause intermediate sections to become visible and fire requests along the way.

Therefore:

```text
click #related_lives
-> observed video + author + live requests
```

must **not** be interpreted as “LIVE requires the video and creator endpoints.”

The experiment combines:

- runtime endpoint observation;
- isolated/repeated section tests;
- route-module static wrappers;
- business access codes;

instead of deriving architecture from scroll order alone.

## 12. Canonical decomposition proposed by FM-004

The vendor page should be decomposed approximately as:

```text
ProductIdentity
ProductMetadataObservation
ProductAggregateObservation
ShopIdentity
ShopAggregateObservation

ProductCreatorRelationshipObservation
ProductVideoRelationshipObservation
ProductLiveRelationshipObservation
LiveSession

ProductHistoryCapability
PaidTrafficCapability
ReviewCapability
SimilarityCapability
VOCCapability
SKUCapability
```

No single `Product` table should absorb all of these grains.

## 13. Redesign classification

```text
Product identity / upstream URL     -> KEEP + INTERNALIZE
Product aggregate facts             -> KEEP + INTERNALIZE pending upstream proof
Shop relationship                   -> KEEP + INTERNALIZE
Creator relationship graph          -> KEEP + INTERNALIZE
Video relationship graph            -> KEEP + INTERNALIZE
LIVE relationship graph             -> KEEP + INTERNALIZE
Monolithic long Product Detail UI   -> COMPRESS
Manual section navigation           -> DROP as primary interaction model
Overview charts                     -> REBUILD only from owned history if useful
Paid traffic module                 -> MODEL/UPSTREAM STUDY
Reviews/VOC                         -> DEFER until internal decision value is proven
Similar-products UI                 -> REBUILD as graph/query if useful
Vendor entitlement machinery        -> DROP from canonical design
```

## 14. Most important upstream clue

`baseInfo` directly provides the official TikTok Shop product URL for the same product ID.

This gives Source Forensics a clean next step:

```text
FastMoss Product
  -> product ID 1731916815699052495
  -> TikTok Shop product URL
  -> official/public upstream observations
```

We can now start asking which FastMoss primitives are simply normalized TikTok facts and which require FastMoss historical collection or models.

## 15. Unknowns carried forward

- exact semantic grain of broad creator/video/LIVE counts;
- source and derivation of cumulative sold count;
- source and derivation of GMV;
- source of creator/product/video/LIVE relationships;
- timezone and attribution rules for relationship windows;
- whether video `estimate_cost_amount` and ROAS are modelled and by what observable inputs;
- what `base.live_count=0` specifically represents;
- upstream availability of reviews/rating/category/price/seller identifiers;
- what history must be accumulated locally to reproduce 7/14/28-day metrics.

## Decision

FM-004 is sufficient to begin vertical upstream attribution for Product rather than continuing to copy additional FastMoss screens blindly.

The next highest-value question is no longer “what does FastMoss show?” but:

> which of these Product primitives can be obtained directly or reconstructed from TikTok Shop/public official surfaces, and which require our own longitudinal history or modelling?

## Next experiment

**FM-005 / TikTok Product upstream attribution.**

Use the official TikTok Shop detail URL exposed by FastMoss and compare, field by field:

- product identity;
- seller/shop identity;
- title/category;
- price;
- rating/reviews;
- cumulative sold count where observable;
- product availability/state;
- creator/video/LIVE relationship primitives where discoverable.

The deliverable will classify the first Product fields as:

```text
DIRECT_UPSTREAM
NORMALIZED
HISTORICAL_DERIVATION_CANDIDATE
MODEL_CANDIDATE
VENDOR_ONLY_UNKNOWN
```
