# Display-only fallback verification

Baseline: `12db88f9d8d8da4591bd517cade159bfef5fcff3` on `feature/verified-code-descriptions`.

Entries without an accepted official description now display `<raw_code> — Description unavailable`. Null, empty or whitespace-only raw codes display `Code not recorded — Description unavailable`. Source values are not trimmed, replaced or normalized; the blank check affects presentation only. The wording describes description availability, not whether an incident is unknown or a code can be classified. No broad-family inference is implemented.

## Actual checks

- All 479 ordered keys, original four source fields and code_description values remain identical to the baseline.
- All 342 accepted dimension rows, including existing display labels, remain identical.
- Exactly 137 display labels change: 135 absent mappings, the conflicting LRT EXVE entry and one missing-code bucket. Their descriptions remain null.
- All nine other CSV exports and every other typed JSON table remain identical.
- Compatible fact totals remain 176,004 incidents, 2,740,515 recorded minutes and 49,830 zero-minute records. Official-description coverage remains 165,124 / 176,004 (93.82%).
- The pinned references, recovery allowlist, raw files, provenance, databases, analytical SQL, Power Query and DAX files retain their baseline checksums.
- Two fresh complete export bundles are byte-identical, including typed JSON and manifest. All manifest export hashes verify. Only DimCode CSV, typed results and the manifest were promoted into the approved bundle after checks passed.
- Full suite: 76 tests pass. Existing missing, ambiguous and encoding-defective label expectations were updated; two new tests cover null/empty/whitespace codes and preservation of all actual accepted descriptions/labels and dimension identities.

## Commands executed

```sh
python3 -B -m unittest discover -s tests -q
python3 -B scripts/export_power_bi.py --output /tmp/ttc-display-fallback-first-20261027
python3 -B scripts/export_power_bi.py --output /tmp/ttc-display-fallback-repeat-20261027
```

Independent read-only Python assertions compared baseline Git JSON, file-checksum inventory and both fresh bundles before promotion. Export verification also checks selected snapshots, lineage, eligibility, relationships, SQLite integrity and foreign keys.

No Power BI schema or measure change is needed for the existing six-column DimCode query. Copy the reviewed complete bundle, verify manifest checksums and refresh manually. Desktop/PBIX was not modified or executed. No files were staged, committed or pushed as part of this implementation.
