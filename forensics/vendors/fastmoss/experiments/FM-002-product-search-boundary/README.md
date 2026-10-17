# FM-002 — FastMoss Product Search Boundary and Backend Contract

## Question

When a visitor reaches FastMoss Product Search, what route/authentication boundary, data transport, request contract, response schema, pagination semantics and client modules can be demonstrated without an authenticated account?

## Status

**Answered for the default Product Search data path.**

The public visitor surface exposes a real Product Search dataset and a much richer backend response than the table renders. This experiment does **not** establish the origin or correctness of FastMoss metrics; that is the purpose of subsequent upstream/field-semantics experiments.

## 1. Product Search is reachable as a visitor

Direct navigation to:

```text
https://www.fastmoss.com/pt/e-commerce/search
```

loads the product-search application and displays a visible permission warning:

> Atualmente, você é um visitante, sem permissões suficientes. Faça login/cadastre-se.

Despite that warning, the visitor UI renders a real product ranking table with products, shops and numerical metrics.

Observed columns include:

- product;
- associated shop;
- influencer conversion rate;
- 7-day sales trend;
- 7-day units;
- 7-day revenue;
- total units;
- total GMV;
- affiliated influencers.

The exact scope of visitor restrictions is **not** inferred from the warning. Export, actions, deeper pages and maximum pagination remain separate questions.

## 2. The data is not in the initial HTML document

A supplemental CDP capture retained the initial `Document` body after a clean reload.

The document contains:

- Next.js / React Server Component bootstrap data (`self.__next_f.push`);
- filter/table structure;
- labels and column headings;
- visitor permission text.

It does **not** contain the product IDs or product names that later appear in the hydrated table.

Therefore the product rows are dynamic client-side data, not simply server-rendered into the initial HTML.

The raw document is retained locally under `evidence/raw/` and only its hash/proof summary is versioned.

## 3. Product Search backend endpoint

Browser `PerformanceResourceTiming`, followed by a REA passive experiment during UI pagination, identified the primary search request:

```text
GET /api/goods/V2/search
```

Observed default functional parameters:

```text
page=<n>
pagesize=10
order=2,2
region=US
```

The public web client automatically adds volatile request parameters:

```text
_time=<Unix seconds>
cnonce=<client-generated random integer>
```

Page 2 was observed by REA as:

```text
XHR
HTTP 200
application/json
```

with runtime initiator:

```text
/_next/static/chunks/65348-7e4132441d123039.js
line 20, column 46189
```

## 4. Pagination is real, not merely cosmetic

UI-driven requests were observed for pages 2, 3, 4 and 5.

The page-5 response differs in SHA-256 and product IDs from the page-3 response, so the `page` parameter demonstrably selects different data.

The response reports:

```text
data.total_cnt = 5000
data.total_cnt_show = "5.0 mil"
```

The UI displays 500 pages at `pagesize=10`. This does **not yet prove** that a visitor is authorized to traverse all 500 pages; only ordinary pagination behavior has been established.

## 5. Response structure

A REA body-shape capture of page 2 observed:

```text
root: object
node_count: 1482
max_depth: 6

data.product_list: array[10]
data.ext: object
data.is_ai: boolean
```

`data.ext` contains observed fields including:

```text
is_ok
took
total_cnt
total_cnt_show
```

The Product Search records expose **63 first-level fields** in the observed response. The complete typed inventory is stored in `artifacts/product-search-schema.json`.

Important metric families include:

```text
yday_sold_count / yday_sale_amount
day7_sold_count / day7_sale_amount
day14_sold_count / day14_sale_amount
day28_sold_count / day28_sale_amount
sold_count / sale_amount
relate_author_count
relate_video_count
relate_live_count
author_order_rate
trend
```

and identity/context fields including:

```text
id
product_id
title
region
category_name L1/L2/L3
shop_info
currency
price
crate
launch_time
product_rating
```

Most metrics also have a parallel `*_show` presentation field. Canonical Source Forensics modeling should prefer raw numeric fields and treat presentation strings as display evidence, not primary facts.

## 6. Real response values were confirmed

A UI-driven CDP capture of a normal pagination request retained a response body locally and produced a compact summary.

Observed response characteristics:

```text
code = 200
msg = "success!"
product_count = 10
total_cnt = 5000
is_ai = false
```

The response contains actual numeric values for 7/14/28-day units/GMV, lifetime units/GMV, creator/video/LIVE relationships, commission, shop information and conversion-rate-style fields.

This proves these are real response fields in the visitor context. It does **not** prove that the metrics are direct TikTok facts, accurate estimates, historical derivations, or model outputs.

## 7. Client implementation semantics

The Product Search page-specific Next.js chunk contains a direct wrapper equivalent to:

```text
GET /api/goods/V2/search with supplied params
```

The page component constructs defaults equivalent to:

```text
page = 1
pagesize = 10
order = 2,2
region = current region (when not Global)
+ URL search parameters
```

and refreshes the query when any of these change:

- current region;
- URL query/filter state;
- current user level.

This explains two key architectural facts:

1. the URL/querystring is part of the declarative filter state;
2. plan/user-level changes can alter data-fetch behavior even on the same route.

## 8. Filters are encoded as query state

The shipped Product Search module contains filter mappings for:

- category hierarchy (`l1_cid`, `l2_cid`, `l3_cid`);
- date window (`last_date_type`, 7 vs 28);
- 7/28-day GMV;
- 7/28-day units;
- total GMV;
- total units;
- related video count;
- related author count;
- price;
- commission;
- commerce/sales format;
- launch date;
- full-service-shop status for supported regions.

Filter changes update `URLSearchParams`, reset `page=1`, and therefore become backend query parameters on the next search request.

## 9. HTTP client contract

The shared browser client adds:

```text
_time
cnonce
region header
lang header
source=pc header
fm-sign header
fm-sig header
```

Runtime page-4 evidence confirmed:

```text
region: US
lang: PT_BR
source: pc
fm-sign: present, 32 characters
fm-sig: present, 64 characters
Cookie header: absent on the observed visitor request
```

The shipped client contains the corresponding request/signature-generation logic. Source Forensics records that behavior as architecture/evidence but **does not build its production data plane around reproducing a proprietary vendor-signing mechanism**. Our intended direction remains upstream acquisition and independent reconstruction.

See `artifacts/http-client-contract.json`.

## 10. Search UI is a projection of a richer contract

The visible table consumes only a subset of `product_list`.

The backend response already includes data that the default table does not expose prominently, including 14/28-day metric families and multiple relationship counts.

This validates an important redesign principle:

> do not copy the vendor's screens; identify the smallest canonical data model that can generate the useful views and signals.

## 11. Adjacent Product Search calls

Browser runtime also observed:

```text
/api/goods/filterInfo?region=...
/api/search/history?type=3
/api/agent/pageSuggestList?page_location=good_search&region=...
/api/user/index/userInfo
/api/author/index/country
```

These should remain separate capabilities:

- filter taxonomy / available value ranges;
- search history;
- agent suggestions;
- user state;
- country/region metadata.

They are not part of the core product-row response merely because the page calls them.

## 12. Information learned about the surrounding client

The page is built from:

- a route-specific Product Search chunk;
- shared table/filter components;
- a shared HTTP client/signing middleware;
- Ant Design pagination/table components;
- Next.js route/query state.

No real-site source maps were available, so runtime callsites + exported minified chunks remain the primary code evidence.

Third-party bundle bytes are intentionally not committed to this public repository. We keep URLs, hashes, Evidence IDs and semantic extracts instead.

## 13. Unresolved questions

FM-002 deliberately does not answer:

- whether `day7_*`, `day14_*`, `day28_*` are direct, snapshot-derived, or modelled;
- what `author_order_rate` precisely means;
- what `crate` represents semantically beyond the UI's commission label;
- how `trend[]` is produced;
- where shop/product IDs originate upstream;
- whether FastMoss can expose all 5,000 ranked products to visitor accounts;
- which filters or operations are plan-restricted;
- whether values differ by user level;
- how current FastMoss values compare with TikTok/other primary sources.

These become falsifiable field-semantics/upstream experiments rather than guesses.

## Decision

**Product Search is important enough to reproduce conceptually.**

What we want to own is not the FastMoss endpoint. We want to own the canonical primitives and historical observations capable of generating equivalent or better search/ranking intelligence.

Current redesign classification:

```text
Product Search UI          -> COMPRESS
Product/Shop identities    -> KEEP / INTERNALIZE
Historical sales windows   -> INTERNALIZE pending upstream proof
Relationship counts        -> INTERNALIZE pending upstream proof
FastMoss request contract  -> FORENSIC BENCHMARK, not production dependency
Export UI                   -> DROP/DEFER until internal use requires it
500-page manual navigation  -> DROP as interaction model
```

## Next experiment

**FM-003 — Product Search filter and temporal semantics.**

Prove how region (starting with Brazil), 7-day vs 28-day windows, sorting and representative filters map into backend parameters and response fields. This experiment will begin separating UI semantics from the canonical metric model and prepare the first upstream-attribution study.
