# Open Victorian property-price baseline

The Observatory has an independent, automatically refreshable historical-price layer with **no realestate.com.au dependency**.

## Origin and licence

The original publisher is the Department of Transport and Planning, Victorian Government. The data are from Valuer-General Victoria's published annual suburb median series, licensed under Creative Commons Attribution 4.0. National Digital republishes a normalised, versioned copy at publicdata.au.

- Houses: https://publicdata.au/d/vic-median-house-prices-by-suburb/
- Units: https://publicdata.au/d/vic-median-unit-prices-by-suburb/
- Official catalogue: https://discover.data.vic.gov.au/
- Licence: https://creativecommons.org/licenses/by/4.0/

Each record has `locality`, `year`, and `median_price`. Suppressed median values remain empty/null. Suburb medians are **not** matched individual sales and cannot supply auction passed-in rates, genuine bids, indicative range, reserve, or post-auction sale prices.

## Automation

Workflow: `.github/workflows/open-vic-data.yml`

It checks latest publicdata.au house/unit tables each Sunday and Wednesday in UTC, validates row counts/columns and writes changed CSVs to `data/open/`, preserving a SHA-256 hash, source version, retrieval timestamp and CC BY attribution in `provenance.json`. New revisions also remain in Git history.

The workflow also supports manual dispatch via GitHub > Actions. It uses GitHub's automatically provided `GITHUB_TOKEN` to commit updates; no personal API key is required. GitHub Actions schedules may start late or be disabled after inactivity; treat workflow-run logs as the source of truth. The government datasets generally change yearly. **This is a scheduled freshness check, not a weekly auction-result feed**.

For direct API exploration without downloading CSV, use the documented publicdata.au API, for example:

```text
https://publicdata.au/api/v1/datasets/vic-median-house-prices-by-suburb/aggregate?group=locality&metric=max.median_price&year=eq.2025
```

The first successful GitHub Action should be verified before claiming that the data is collecting automatically.

## Auction collection remains pending

The permissioned Cloudflare aggregate collector is separately prepared but not deployed. Domain has a documented weekly sale-results API; the terms and the Cloudflare data-residency issue must be resolved before connecting it. See `docs/DATA_SOURCES.md`.
