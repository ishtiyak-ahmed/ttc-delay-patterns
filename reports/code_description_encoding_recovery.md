# Reviewed code-description encoding recovery

Baseline: `d608986ee9a67aa7247d57749262002d516e55c5` on `feature/verified-code-descriptions`. No commit, push or Desktop/PBIX changes were made.

## Scope and mechanism

The 56 observed encoding-defective mode/code entries are explicitly listed in `config/code_description_recovery.json`, separately from the immutable official references. Each entry records original text, expected recovered text and resource SHA-256. Shared metadata records reference version, reference-manifest SHA-256 and recovery method.

Only these entries can recover the exact Unicode sequence U+00E2 U+0080 U+0093 to U+2013 (en dash). Strict Latin-1 encoding / UTF-8 decoding must reverse exactly, match the recorded expected text and change nothing except that sequence. Surrounding text must be ASCII for this reviewed mechanism; unsupported input fails closed. Recovery cannot target already accepted, missing or conflicting descriptions. The original rows are copied in memory and existing blank, ambiguity and encoding acceptance checks run again afterward.

All 56 recoveries are punctuation-only: 55 descriptions contain one corrupted dash and Subway PUTSC contains two. PUTSC becomes `SIGNALS–CONTROL PROBLEM–TRACK` without inserted spaces. Source typos, including Streetcar `INJURIED` and `AVILABLE`, are preserved. No general Unicode normalization, case conversion, typo repair, suffix interpretation or broad-family classification is performed.

All source dictionaries, their manifest and historical `mapping_issues.json` remain byte-identical. That historical inventory still documents the original source defects; the regenerated export manifest supplies current acceptance, unresolved mappings and a hash of the separate recovery evidence. Four additional defective reference entries not among the 56 observed entries remain unrecovered by design.

## Actual coverage

| Mode | Newly recovered codes | Newly covered records | Accepted codes before → after | Incident coverage before → after |
| --- | ---: | ---: | ---: | ---: |
| Bus | 10 | 15,001 | 30 → 40 | 79.98% → 94.65% |
| Streetcar | 13 | 3,970 | 61 → 74 | 69.64% → 86.39% |
| Subway | 33 | 12,440 | 97 → 130 | 69.01% → 96.36% |
| LRT | 0 | 0 | 98 → 98 | 88.36% → 88.36% |
| Total | 56 | 31,411 | 286 → 342 | 75.97% → 93.82% |

Accepted descriptions cover 165,124 of 176,004 records. Remaining unresolved: 135 absent mode/code mappings covering 10,878 records, LRT EXVE covering one record, and the Streetcar missing-code bucket covering one record. No discrepancy from expected coverage was found.

## Executed verification

```sh
python3 -B -m unittest discover -s tests -q
python3 -B scripts/export_power_bi.py --output /tmp/ttc-encoding-recovery-first-20261027
python3 -B scripts/export_power_bi.py --output /tmp/ttc-encoding-recovery-repeat-20261027
```

The full suite passes 74 tests (66 existing plus eight new regression tests). The existing pinned-reference expectation was updated for the now-recovered Bus MFUIR description. Tests cover all 56 reviewed texts, double-dash recovery, source typos, all 286 previously accepted observed descriptions, original dimension fields/keys, immutable input rows, unsupported corruption/native Unicode, incomplete or duplicate allowlists, incorrect hashes/version/method, altered original/expected text, cross-mode misselection, conflicts and deterministic recovery.

Independent Python reconciliation compared both fresh exports against the baseline Git/byte inventory before promoting only `dim_code.csv`, `results.json` and `manifest.json` into the approved bundle:

- All 479 ordered keys and original four DimCode columns are identical. Only description/display-label values of the 56 reviewed rows change; the other 423 complete dimension rows are identical.
- All 286 previously accepted descriptions and labels remain identical.
- All nine other CSV exports are byte-identical; every other typed JSON table is identical.
- All compatible fact partitions retain 176,004 incidents, 2,740,515 recorded minutes and 49,830 zero-minute records.
- Full repeated bundles, including manifest and typed JSON, are byte-identical; export hashes match the manifest.
- Original reference-directory files, raw datasets, provenance, staging/curated databases, analytical SQL, Power Query and DAX files retain their baseline hashes.
- Export verification confirms selected snapshots/lineage, valid relationships, unique fact/dimension grains, SQLite integrity and zero foreign-key violations.

## Handoff and limitations

Changes are limited to recovery evidence, the enrichment/export modules, regression tests, these verification notes, the contract documentation and three generated bundle files. The 14 proposed broad-family inferences remain unimplemented.

For an existing six-column DimCode import, no schema change is needed: copy the reviewed complete bundle, check checksums and manually refresh Power BI. Repository checks do not execute Desktop or DAX. Recovery restores source wording, not verified causes or historical validity. Future reference versions or other encoding defects require a separate review; the allowlist does not expand automatically.
