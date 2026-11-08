# Victorian Auction Observatory

A research system for tracking Victorian auction-result revisions and, once authorised property-level data is available, vendor expectations, post-auction conversion and price realisation.

**Status (8 November 2026): research/architecture stage. Cloudflare is NOT deployed. No live auction collection is active.**

## Data sources

| Source | Useful fields | Access status |
| --- | --- | --- |
| Domain developer API: `GET /v1/salesResults/{city}/listings` | Sold prior/at/after, passed in, withdrawn, highest bid, vendor bid, listing identifiers | Documented, but an approved API purpose/licence is required. Don't collect automatically until storage/analysis rights are confirmed. |
| REIV PropertyData | Auction outcomes, historical property sales | Commercial/permissioned enquiry required |
| Cotality weekly summaries | Preliminary and final market aggregates | Public viewing; automated reuse not established |
| Valuer-General Victoria / DataVic | Suburb medians and quarterly/annual sales volumes | Government open datasets, some CC BY 4.0. Suitable for freely licensed historical baseline |
| LANDATA | Authoritative sale history | Paid and eligibility-restricted; individual reports differ from licensed bulk access |

**Important:** Domain API terms include limits on derivative works, third-party access and storage outside Australia. Cloudflare D1's Oceania *location hint* is not an Australia-only residency guarantee. Do not connect Domain data to Cloudflare without explicit permission covering the proposed storage and use.

## Planned indices

- VEI: Vendor Expectations Index — disclosed reserve vs earlier indicative selling range.
- PASCI: Post-Auction Sale Conversion Index — conversion of failed auctions over fixed follow-up windows.
- PRI: Price Realisation Index — sale price relative to indicative range and reserve, by sale pathway.

Do not calculate any of these from weekly headline aggregates; property-level observations are required.

## Revision capture

Scheduled candidate slots in Melbourne local time: Sunday 12:17, Sunday 19:17, Monday 09:17, Wednesday 19:17, Thursday 10:17. Preserve immutable observations, publisher timestamps, status (including missing/late reports), data provenance, and per-source methodology. Unknown ≠ zero.

## Deployment plan

The v0.2 code package, prepared separately, includes a Cloudflare Worker, D1 migrations, immutable aggregate snapshots, a protected browser importer, a health dashboard and tests. Source code is not yet imported into this new repository. Deployment will be controlled by GitHub Actions and disabled until Cloudflare secrets/vars are configured.

1. Import the v0.2 project tree from the prepared package, preserving `.github/workflows/cloud.yml` and `cloud/`.
2. Create the Cloudflare D1 database `victorian-auction-observatory`.
3. Add restricted Cloudflare deployment credentials as GitHub Actions secrets; never commit tokens.
4. Enable the explicit deploy variable once reviewed.
5. Start with freely licensed government baseline data and an authorised/manual snapshot feed.
6. Seek written Domain/REIV permission for property-level auction and subsequent sale-price history.

## Primary reference links

- [Domain results endpoint](https://developer.domain.com.au/docs/latest/apis/pkg_properties_locations/references/salesresults_listings/)
- [Domain API terms](https://www.domain.com.au/group/api-terms-and-conditions/)
- [REIV PropertyData](https://reiv.com.au/business-services/property-data)
- [Valuer-General Victoria sales statistics](https://www.land.vic.gov.au/valuations/resources-and-reports/property-sales-statistics)
- [DataVic catalogue](https://discover.data.vic.gov.au/)
- [Cloudflare D1 location constraints](https://developers.cloudflare.com/d1/configuration/data-location/)
