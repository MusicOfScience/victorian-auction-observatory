# Data access audit — 8 November 2026

## Decision

Do **not** scrape realestate.com.au or Domain websites. The project should begin with Victorian government CC BY 4.0 suburb statistics and synthetic or separately authorised auction captures. Property-level auction research needs explicit feed rights.

## Highest-priority candidate: Domain sales-results API

Official endpoint: https://developer.domain.com.au/docs/latest/apis/pkg_properties_locations/references/salesresults_listings/

Required OAuth/API scope: `api_salesresults_read`. The documented endpoint is `GET /v1/salesResults/{city}/listings`, returning the **last sales-result reporting period**. The documentation does *not* establish a historical arbitrary-date endpoint. Domain's consumer website provides six months of selectable auction weeks, but that does not grant API historical access or collection rights.

Documented outcome codes:

| Code | Interpretation |
|---|---|
| AUSD, AUSN | Sold at auction; price = sale price |
| AUSA, AUSS | Sold after auction; price = sale price |
| AUPN, AUSP | Sold prior; price = sale price |
| AUHB | Highest bid below reserve; price = reported bid |
| AUPI | Passed in; no price |
| AUVB | Vendor bid; price is not genuine buyer willingness |
| AUWD | Withdrawn; no price |
| PTSD, PTSW, PTLA | Private treaty variants; not substitutes for auction outcomes |

The listing summary includes a listing ID, locality, property type, beds/baths/car spaces, agency and listing URL. There is **no verified original indicative range or reserve field in this weekly result response**. An additional authorised feed or agent partnership would be required.

Commercial and technical questions for Domain:

1. Is `api_salesresults_read` available to an independent, non-commercial Victorian research project? At what price and quota?
2. Are Sunday, Monday, Wednesday revisions exposed for the same auction week? Does a historical week parameter exist?
3. Are agent price guide revisions, Victorian Property Price Statements and reserves licensed for access? How are revisions timestamped?
4. May we retain immutable historical observations and compute VEI/PASCI/PRI derivatives? May aggregate analyses be published?
5. Do we need Australian-only hosting? Can written permission vary the standard API restriction on accessing, using and storing API data outside Australia?
6. Can the feed include later private sales of properties initially passed in, with stable property identifiers?
7. What attribution, retention, deletion and licence-termination rules apply?

Standard Domain API terms: https://www.domain.com.au/group/api-terms-and-conditions/

**Critical hosting caveat:** Cloudflare D1 has an `oc` (Oceania) *hint*, but not an Australian residency guarantee. Supported D1 hard jurisdictions are EU, US and FedRAMP. Do not ingest Domain data in D1 until rights and residency are settled.
https://developers.cloudflare.com/d1/configuration/data-location/

## Other source candidates

### REIV PropertyData
- https://reiv.com.au/business-services/property-data
- High claimed auction coverage, historical sales, agent-submitted records.
- Ask for research pricing, property-level export, revisions, original range, reserve and retrospective matched sale event.
- Ask whether derived aggregated indicators may be published.

### Cotality
- https://www.cotality.com/au/our-data/auction-results
- Preliminary and final aggregate auction summaries. Can compare methodologies; third-party copyright restrictions apply.
- Investigate licensed Auction API; do not assume freely accessible public pages permit database harvesting.

### Valuer-General Victoria / DataVic
- https://www.land.vic.gov.au/valuations/resources-and-reports/property-sales-statistics
- https://discover.data.vic.gov.au/dataset/victorian-property-sales-report-yearly-summary
- Suburb-level annual and quarterly datasets, some CC BY 4.0 with attribution. Good *open* baseline; cannot identify individual no-bid auctions or subsequent sales.
- Refresh on publication/update, not weekly as the datasets are not weekly.

### LANDATA
- https://www.landata.online/victorian-property-sales-data/
- Authoritative individual sale history. Professional/bulk eligibility restricted; members of public can buy individual reports. Not a free unrestricted bulk dataset.
- Settlement/validation lag matters for event-time measures.

## Minimal viable research pipeline

**Track A (unblocked):** Acquire CC BY 4.0 government reference datasets, store source/version hashes, source dates, licence attribution and suburb/house-unit granularity. Government figures are not Sunday auction revisions; keep a separate namespace and cadence.

**Track B (permissioned):** Run Sunday 12:17 and 19:17, Monday 09:17, Wednesday 19:17, Thursday 10:17 Melbourne-local capture on a licensed weekly-auction feed. Preserve snapshots, reporting status, missingness, source methodology and category revisions. Cloud collector must not invent real observations when no feed exists.

**Track C (research):** Capture pre-auction indicative ranges, published reserves, highest genuine bid, genuine bidder count, sale time and achieved price per property. Follow passed-ins at 7/30/60/90 days. No property-level index until these measures have defensible coverage.

## Launch guardrails

- No secret or proprietary record in public GitHub.
- No claimed data coverage until licensed live pulls succeed.
- Never assume `null` means zero.
- Keep source-specific reporting denominators separate.
- Licence and hosting agreement must permit storage, derivatives and intended display.
- A 'sold after' reported in the auction week is distinct from a sale 30 days later.
- Confirm 30/90-day cohorts are mature before reporting conversion fractions.
