# Verified DimCode enrichment

Baseline: clean `main` at `76837af53f4e088290c02a8d2f76d61e19adfc2e`. Work is on `feature/verified-code-descriptions`; no commit, merge or push was performed.

## Reference evidence and matching

The four official City of Toronto/TTC dictionaries are preserved byte-for-byte under `references/ttc_delay_codes/2026-10-26/`. The manifest records exact package/resource IDs, source and final URLs, UTC retrieval timestamps, HTTP 200 responses, sizes, SHA-256 checksums and available headers. Certificate and hostname verification remained enabled using the existing certifi bundle. Bus and Streetcar use official JSON downloads, LRT the official CSV datastore dump, and Subway a complete official CKAN JSON response. Network timeouts preceded successful retrievals; Bus retrieval succeeded. Bus response headers were not captured and are explicitly empty in the manifest. Retrieval occurred on October 26 Toronto time / October 27 UTC.

Matching uses exact `(source_mode, raw_code)` only. Identical dictionary pairs collapse to one lookup entry, never to fewer incident records. Conflicting descriptions, missing descriptions, absent mappings and detected encoding corruption receive no accepted description. No case, whitespace, punctuation or encoding repair is performed. Original reference text and all observed unresolved codes, weighted by incident records, are retained in `references/ttc_delay_codes/2026-10-26/mapping_issues.json`.

`code_description` contains accepted source text or null (blank CSV cell). `code_display_label` is raw code plus an em dash and accepted description; unresolved values retain their raw code. The existing missing-code bucket displays `[Missing code]`. Neither attribute is a relationship key or a verified causal interpretation.

## Description coverage

Code denominators below exclude the existing missing-code bucket; incident denominators include every source record. Coverage measures reference acceptance, not analytical eligibility.

| Mode | Accepted / nonblank codes | Covered / all incident records | Incident coverage |
| --- | ---: | ---: | ---: |
| Bus | 30 / 75 | 81,788 / 102,257 | 79.98% |
| Subway | 97 / 140 | 31,381 / 45,475 | 69.01% |
| Streetcar | 61 / 148 | 16,507 / 23,703 | 69.64% |
| LRT | 98 / 115 | 4,037 / 4,569 | 88.36% |

There are 286 accepted dimension rows covering 133,713 records. The remaining 193 dimension rows comprise 135 unmapped codes, 56 encoding-defective descriptions, one ambiguous code and one missing-code bucket. LRT `EXVE` has conflicting official descriptions and remains unresolved (one observed record). LRT `TXSUP` has identical repeated reference entries and can be accepted once. Bus `MFDV` is matched to its Bus dictionary; descriptions are never borrowed between modes. Encoding detection is conservative and cannot establish that every undetected source spelling is correct. Dictionary publication dates do not establish historical validity for every incident date.

## Executed verification

Commands:

```sh
python3 -B -m unittest discover -s tests -v
python3 -B scripts/export_power_bi.py --output /tmp/ttc-code-enriched-power-bi
python3 -B scripts/export_power_bi.py --output /tmp/ttc-code-enriched-repeat
```

Additional read-only Python comparisons used the baseline Git export, initial file SHA-256 inventory, generated manifest and both fresh export directories. Only the reviewed DimCode CSV, typed results JSON and manifest were promoted into the existing bundle.

- All 66 tests pass (58 existing, eight focused enrichment tests). New tests cover missing, duplicate, ambiguous, cross-mode and encoding-defective mappings, original-column preservation, reference integrity and invalid keys.
- All 479 original dimension keys, ordered rows and four original columns match the baseline exactly. Only two columns are appended.
- All nine other CSV exports are byte-identical. All other typed export tables are identical.
- Fact totals remain 176,004 recorded incidents, 2,740,515 recorded minutes and 49,830 zero-minute records.
- Repeated complete exports are byte-identical, including manifest and typed JSON. Export checksums match the new manifest.
- Raw files, staging/curated database files, existing DAX definitions and validation queries retain their baseline checksums. No source manifest, SQL calculation, fact or relationship key was changed.
- Removing only the two appended import type declarations recreates the original Power Query implementation exactly.

The exporter verifies the pinned reference checksums and complete four-mode presence on each run. Its manifest identifies reference and implementation hashes and reports accepted/unresolved coverage.

## Desktop handoff and limits

Use the exact existing-query edit in [the Desktop build instructions](../docs/power_bi_desktop_build.md#additive-dimcode-refresh--2026-10-26): append the two Text attributes to the existing DimCode `ReadTtcCsv` schema list, then Close & Apply / refresh. Do not recreate queries, keys, relationships or measures. Existing strict header checks require this schema addition before refresh. Visuals may optionally use `code_display_label`; retain mode context and avoid description-only identity or unsupported cross-fact filtering.

No PBIX or Desktop session was modified. The user's previously validated 10 queries, 13 relationships and 54 measures must be reconfirmed manually after refresh. Repository checks establish unchanged data, keys and definitions, but do not execute Power Query or DAX in Desktop. Compare the same code-key selections before/after, including unresolved codes, missing codes, independent route panels and Bus-MFDV measures. Source ambiguities and encoding defects remain unresolved pending official clarification; no additional cleaning rules were introduced.
