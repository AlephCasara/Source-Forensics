# FM-003 — FastMoss Product Search Filter and Temporal Semantics

## Question

How do region, 7-day vs 28-day windows, default sorting and representative filters map from Product Search intent into backend parameters and response semantics?

## Status

**Answered for Brazil, the 7/28-day window switch, default units-sold sort and one representative units-sold filter.**

This experiment turns several vendor-specific fields into a smaller canonical metric model.

## 1. Region is an explicit analytical dimension

Controlled browser navigation to Product Search with:

```text
region=BR
```

produced a backend request containing:

```text
region=BR
```

and the runtime request header also contained:

```text
region: BR
```

All observed products in both 7-day and 28-day response samples reported:

```text
region = BR
```

The visitor request still carried no `Cookie` header in these captures.

### Design implication

`region` belongs in the canonical observation/metric dimensions. It must not be embedded in vendor-specific endpoint schemas or duplicated in separate regional tables.

## 2. `last_*` is a contextual vendor alias

For an explicit 7-day Product Search:

```text
last_date_type=7
```

all 10 observed records satisfied:

```text
last_sold_count  == day7_sold_count
last_sale_amount == day7_sale_amount
```

For an explicit 28-day Product Search:

```text
last_date_type=28
```

all 10 observed records satisfied:

```text
last_sold_count  == day28_sold_count
last_sale_amount == day28_sale_amount
```

Seven products occurred in both top-10 samples, and their underlying `day7_*`, `day28_*`, total `sold_count` and total `sale_amount` values remained stable across the two requests while `last_*` switched to the selected window.

### Conclusion

Within the observed Product Search contract:

```text
last_sold_count(window=7)  := day7_sold_count
last_sold_count(window=28) := day28_sold_count

last_sale_amount(window=7)  := day7_sale_amount
last_sale_amount(window=28) := day28_sale_amount
```

`last_*` should therefore **not** exist in our canonical semantic layer. It is a presentation/query convenience in the vendor contract.

## 3. The selected window changes ranking semantics

The 7-day and 28-day top-10 lists were not identical and their ordering changed.

In both captures, the returned `last_sold_count` values were monotonically descending.

The Product Search client code also declares the default sorter over `last_sold_count`, descending, while runtime sends:

```text
order=2,2
```

### Supported interpretation

For this Product Search surface, current evidence supports:

```text
order=2,2
 -> sort by selected-window units sold
 -> descending
```

This mapping is supported jointly by static client evidence and runtime result ordering.

## 4. FastMoss exposes filter taxonomy as data

The page calls:

```text
GET /api/goods/filterInfo?region=BR
```

The response provides the valid filter bands used by Product Search. Examples for Brazil include:

### Windowed units sold

```text
0,500       -> <500
500,1000    -> 500-1 mil
1000,5000   -> 1 mil-5 mil
5000,10000  -> 5 mil-10 mil
10000,-1    -> >10 mil
```

The same bands are exposed separately for `day7_sold_count` and `day28_sold_count`.

### GMV / revenue

Bands are provided for total, 7-day and 28-day sale amount, including ranges such as:

```text
0,1500
1500,5000
...
1000000,-1
```

with localized BRL labels.

### Other filter families observed

- price bands;
- influencer/author order-rate bands;
- related-author counts;
- related-video counts;
- launch-age ranges;
- commission-rate (`crate`) bands;
- total units / total GMV;
- country list including BR and other FastMoss-supported markets.

The compact captured taxonomy is in `artifacts/br-filter-info.json`.

## 5. One user intent maps to different backend fields by window

The same semantic request:

> products with more than 10,000 units sold in the selected window

maps as follows.

### 7 days

```text
last_date_type=7
day7_sold_count=10000,-1
```

Observed:

```text
total_cnt = 21
```

All 10 returned products on page 1 had `day7_sold_count >= 10000`.

### 28 days

```text
last_date_type=28
day28_sold_count=10000,-1
```

Observed:

```text
total_cnt = 319
```

All 10 returned products on page 1 had `day28_sold_count >= 10000`.

### Design implication

The canonical system should represent this as a predicate over a parametrized metric:

```text
windowed_units_sold(window_days=7)  > 10000
windowed_units_sold(window_days=28) > 10000
```

not as two unrelated filter controls or two unrelated data concepts.

## 6. Canonical metric proposal

FM-003 supports the following first semantic compression:

```text
MetricDefinition: windowed_units_sold
  subject: Product
  dimensions:
    - window_days
    - region
    - observed_at
  observed_vendor_windows:
    - 7
    - 14
    - 28

MetricDefinition: windowed_gmv
  subject: Product
  dimensions:
    - window_days
    - region
    - currency
    - observed_at
  observed_vendor_windows:
    - 7
    - 14
    - 28
```

The 14-day raw fields exist in Product Search responses, but the observed Product Search date-window UI exposes 7 and 28 days. We do not yet know whether 14-day data is used by another UI, is legacy/hidden, or is simply an extra backend capability.

## 7. Interaction redesign implication

FastMoss exposes this through several controls and field aliases. Source Forensics should be able to accept one intent such as:

```text
Top Brazilian products by units sold over the last 28 days,
with at least 10,000 units sold.
```

and compile it into the canonical semantic query. UI widgets can exist as optional projections, but they should not define the domain model.

## 8. What this experiment does not prove

This experiment establishes **FastMoss semantics**, not upstream truth.

It does not prove:

- that a FastMoss 7-day count is a direct TikTok field;
- that the window is implemented through historical snapshots versus another upstream primitive;
- exact timezone/window-boundary semantics;
- treatment of refunds, cancellations or returned products;
- how GMV is priced/converted;
- accuracy of FastMoss values.

Those are upstream-attribution and validation questions.

## Decision

Vendor fields are normalized as follows:

```text
last_sold_count       -> DROP as canonical field / map to selected window
last_sale_amount      -> DROP as canonical field / map to selected window
day7_sold_count       -> windowed_units_sold(window=7)
day14_sold_count      -> windowed_units_sold(window=14)
day28_sold_count      -> windowed_units_sold(window=28)
day7_sale_amount      -> windowed_gmv(window=7)
day14_sale_amount     -> windowed_gmv(window=14)
day28_sale_amount     -> windowed_gmv(window=28)
region                -> canonical dimension
range codes           -> adapter-level encoding of semantic predicates
order=2,2             -> adapter-level encoding of sort(windowed_units_sold, desc)
```

## Next experiment

**FM-004 — Product Detail anatomy.**

Follow a real Brazilian product observed in Product Search into Product Detail and determine:

- which backend requests build the detail page;
- which identifiers link Product -> Shop -> Creator/Video/LIVE;
- what temporal/history series are returned;
- what additional fields exist outside Product Search;
- what is public versus permission-gated;
- which fields become the first candidates for upstream attribution.
