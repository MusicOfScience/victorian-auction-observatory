#!/usr/bin/env python3
"""Refresh CC BY 4.0 Victorian suburb median price reference tables.

This is **not** an auction feed: government time series update annually.
The source is the Victorian Government, normalised by publicdata.au.
Do not mix these reference figures with individual auction observations.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "open"
BASE = "https://publicdata.au/d/"
PUBLISHER = "Department of Transport and Planning, Victorian Government"
SOURCES = {
    "house": {
        "slug": "vic-median-house-prices-by-suburb",
        "source": "https://discover.data.vic.gov.au/dataset/victorian-property-sales-report-median-house-by-suburb-time-series",
        "output": "house_medians.csv",
    },
    "unit": {
        "slug": "vic-median-unit-prices-by-suburb",
        "source": "https://discover.data.vic.gov.au/dataset/victorian-property-sales-report-median-unit-by-suburb-time-series",
        "output": "unit_medians.csv",
    },
}


def validate_csv(payload: bytes) -> int:
    """Reject HTML error pages and obviously incomplete/damaged CSVs."""
    if len(payload) > 6_000_000:
        raise ValueError("Unexpectedly large data file")
    text = payload.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text))
    required = {"locality", "year", "median_price"}
    if not reader.fieldnames or not required.issubset(reader.fieldnames):
        raise ValueError(f"Expected CSV fields {sorted(required)}")
    rows = 0
    for row in reader:
        if not (row["locality"] or "").strip():
            raise ValueError("Blank locality")
        year = int(row["year"])
        if year < 1950 or year > 2100:
            raise ValueError("Implausible year")
        price = (row["median_price"] or "").strip()
        if price and int(price) <= 0:
            raise ValueError("Invalid median price")
        rows += 1
    if rows < 200:
        raise ValueError(f"Too few locality/year observations: {rows}")
    return rows


def fetch_dataset(slug: str) -> tuple[bytes, str]:
    url = f"{BASE}{slug}/latest/data.csv"
    request = urllib.request.Request(
        url, headers={"User-Agent": "VictorianAuctionObservatory/0.3 (open-government-data-research)"}
    )
    with urllib.request.urlopen(request, timeout=35) as response:
        if response.status != 200:
            raise RuntimeError(f"Source returned HTTP {response.status}")
        resolved = response.geturl()
        if not resolved.startswith(f"{BASE}{slug}/"):
            raise RuntimeError("Unexpected download redirect destination")
        payload = response.read(6_000_001)
    return payload, resolved


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    manifest_path = DATA_DIR / "provenance.json"
    previous = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    updated = dict(previous)
    dirty = False

    # Validate all sources before writing any files.
    results = {}
    for kind, source in SOURCES.items():
        payload, resolved = fetch_dataset(source["slug"])
        count = validate_csv(payload)
        digest = hashlib.sha256(payload).hexdigest()
        results[kind] = (payload, resolved, digest, count)
        print(f"{kind}: {count} records, SHA256 {digest[:12]}")

    for kind, source in SOURCES.items():
        payload, resolved, digest, count = results[kind]
        path = DATA_DIR / source["output"]
        if path.exists() and hashlib.sha256(path.read_bytes()).hexdigest() == digest:
            print(f"{kind}: unchanged")
            continue
        match = re.search(r"/v/(\d{4}-\d{2}-\d{2})/", resolved)
        version = match.group(1) if match else "unresolved"
        path.write_bytes(payload)
        updated[kind] = {
            "publisher": PUBLISHER,
            "original_dataset": source["source"],
            "normalised_by": "publicdata.au (National Digital)",
            "normalised_url": resolved,
            "version": version,
            "file": source["output"],
            "sha256": digest,
            "rows": count,
            "licence": "CC BY 4.0",
            "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
            "attribution": (
                f"{PUBLISHER}, Victorian Property Sales Report, "
                f"{source['source']}, CC BY 4.0; serialised by publicdata.au."
            ),
        }
        dirty = True

    if dirty:
        manifest_path.write_text(json.dumps(updated, indent=2, sort_keys=True) + "\n")
        print("Updated open-data files and provenance")
    else:
        print("All open datasets unchanged; no commit needed")


if __name__ == "__main__":
    main()
