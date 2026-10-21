# Lossless staging ingestion — Milestone 3, Task 3.2

Completed 2026-10-21. The existing schema v1 is unchanged. Only the four already-downloaded delay snapshots were loaded into SQLite; no network access, semantic cleaning, deduplication or curated transformations were performed.

## Files created or modified

- `scripts/ingest_staging.py`: explicit local-provenance input, validating raw size/hash and manifest identity, strict CSV parsing, parameterized inserts and one transaction per snapshot.
- `scripts/verify_staging.py`: independent, read-only raw-file-to-database comparison, provenance traceability and integrity checks.
- `tests/test_staging_ingestion.py`: 12 deterministic offline tests; existing four foundation tests remain unchanged.
- `reports/staging_ingestion_results.json`: source/staged reconciliation per committed snapshot.
- `reports/staging_verification_results.json`: independent exact-value verification results.
- `reports/staging_ingestion.md`: this handoff and execution record.
- `data/local/ttc.sqlite3`: populated local database, still Git-ignored. Every other pre-existing project file is unchanged, including raw data, provenance, source manifest, schema, initializer, governing documents and profiling results.

## Commands executed

Repository/read checks used `cat`, `git status --short` and Python file inventories, raw SHA-256 checks, provenance inspection and database counts. The database began with all four tables empty. The following commands were executed successfully:

```sh
python3 -m unittest discover -s tests -v
python3 scripts/ingest_staging.py --provenance \
  data/provenance/20261021T190204614685Z__subway.json \
  data/provenance/20261021T190548363172Z__bus.json \
  data/provenance/20261021T190549738480Z__streetcar.json \
  data/provenance/20261021T190550293696Z__lrt.json \
  --report reports/staging_ingestion_results.json
python3 scripts/verify_staging.py --report reports/staging_verification_results.json
```

The original CLI JSON outputs were also inspected. Additional Python assertions compared reconciled counts, blank/zero counts, duration totals and duplicate multiplicities to existing profiles for the same hashes, and checked a pre-task file inventory. These are validation checks, not analytical queries or repeated source discovery.

## Load and reconciliation results

| Mode | Snapshot ID | Actual source rows | Staged rows | Zero Min Delay rows | Repeated-value excess excluding _id |
|---|---:|---:|---:|---:|---:|
| Subway | 1 | 45,475 | 45,475 | 29,669 | 66 |
| Bus | 2 | 102,257 | 102,257 | 12,974 | 298 |
| Streetcar | 3 | 23,703 | 23,703 | 5,279 | 18 |
| Lrt | 4 | 4,569 | 4,569 | 1,908 | 5 |
| Total | — | 176,004 | 176,004 | 49,830 | 387 |

Counts come from the actual preserved files and database, not only the expected-count table. Every snapshot passed exact comparison of all 11 decoded string values and its one-based data-record ordinal. Independent verification compared 1,936,044 field values; all 176,004 staged records trace to a snapshot and successful retrieval event referencing the preserved provenance. Duplicate candidates and their multiplicities remain intact.

Blank strings in all columns were retained exactly. Examples of retained blank direction counts: Subway 15,860; Bus 21,327; Streetcar 5,327; LRT 773. The one blank Streetcar Code remains blank. No values were trimmed, recased, mapped to descriptions, converted to NULL or numerically coerced in staging. `_id` is TEXT and is not an incident identity key.

Source/staged diagnostic Min Delay sums are Subway 122,071; Bus 2,163,102; Streetcar 416,513; LRT 38,829. These checks retain repeated/zero records and are not unique incident counts or service-reliability comparisons. Min Gap is reconciled separately. Date-range diagnostics use the date component and do not establish a source timezone or correct reported Day conflicts.

Database counts: 4 raw_snapshots, 4 retrieval_events, 4 staging_loads, and 176,004 staged_delay_records. The historical failed acquisition JSON was not imported as a successful retrieval. Integrity check: `ok`. Foreign-key violations: 0. No schema changes or new dependencies were necessary.

## Checksums

| Mode | Bytes | SHA-256 |
|---|---:|---|
| Subway | 3069485 | `ec7c36eeb4785e34d58229e5da6af741c89dfdf9fa59c58a63abe5b026b95c44` |
| Bus | 9492730 | `1474f16414e63aaeab58714c236446ea370f5e00e072a3b97fdfeb1f079cd8fe` |
| Streetcar | 1882886 | `c6c081880619ffff8779c61af3a0b77466471473a014d8dec48d16306ddf9606` |
| Lrt | 313915 | `a493ad2f0d3c2889c34eba7cb42b3c27fc1d6cbf15728be09d7f1b230964984a` |

Each hash agrees with the selected preserved provenance and remains unchanged after ingestion. Raw and provenance bytes are checked again before committing a snapshot; snapshot and retrieval identity fields are reconciled with the input metadata.

## Parsing and transaction contract

Inputs are explicit provenance paths relative to the project root. Missing files, unsuccessful provenance, metadata mismatches, size/hash mismatches, duplicate/unexpected headers, invalid UTF-8, malformed CSV syntax and record widths fail clearly. UTF-8-sig decoding removes only an optional initial encoding signature; csv.reader uses strict parsing with newline preservation. Header order is recorded; source values are mapped by exact names. Quoted multiline values are one data record, not multiple physical rows. Numeric/date anomalies are retained as source strings; diagnostic parse results do not filter the data.

For each snapshot, the transaction registers resource/content identity, records the original retrieval/provenance, inserts all raw values and ordinals, reconciles every row and summary, and inserts a successful staging receipt before COMMIT. A malformed later record or failed reconciliation rolls back every database write for that snapshot. Earlier successfully committed snapshots remain if a later selected snapshot fails; this is not an all-four-modes transaction.

The database must first exist with the validated storage foundation; initialization is checked but no schema migration occurs. `(resource_id, sha256)` identifies content and `(snapshot_id, record_ordinal)` identifies a source row. No INSERT OR IGNORE, replacement, upsert or source-field deduplication is used. Report paths use exclusive creation; the CLI refuses an already-existing report path before loading. If a run fails after earlier snapshots commit, the database receipts remain authoritative even if a final combined report was not written.

An already-staged identical snapshot is compared against its source, receipt and retrieval metadata without overwriting anything; incompatible or incomplete existing state is rejected. `--verify-only` performs this selected-snapshot check, while the separate verifier uses a read-only SQLite connection. This minimum guard is required by the existing storage contract; it does not implement monthly/revised-source processing.

## Automated tests

16 tests passed: 12 new staging tests plus four unchanged foundation tests. New tests cover successful fixture ingestion and provenance/ordinal traceability; exact strings, whitespace, blanks, leading zeros, multiline values, duplicate _id/identical rows and invalid semantic values; reordered/duplicate headers; missing raw input; checksum mismatch; malformed width/quoting; invalid encoding; inconsistent source identity; rollback after rows/metadata have been inserted; verification of existing records without rewriting; and detection of a changed staged value despite unchanged row count. Fixtures are isolated in temporary directories and require no network.

## Unresolved questions for Task 3.3

- Actual source revisions, renamed/replacement resources, shrinking coverage and ID reassignment remain unverified. No active-snapshot promotion policy or monthly workflow is implemented.
- The loader requires one matching preserved retrieval event for the selected provenance when checking existing content. Registering another acquisition of identical content, recording load failures persistently, recovery from externally created partial state, and parser-version rebuilds require explicit design in Task 3.3. It refuses ambiguous/incompatible state instead of silently repairing it.
- The default database now has one snapshot per mode. Future outputs must deliberately choose snapshots; summing every version would duplicate history.
- Byte hashes establish file identity, not incident identity. Operational meaning of zeros, extremes, code conflicts and LRT weekday/date conflicts is unchanged by lossless storage.
- Source files are not locked against external editing. The loader parses a captured byte buffer and verifies that raw/provenance bytes still match before commit; filesystem immutability remains a workflow contract.

No commits or pushes were made. Stop after Task 3.2 for review; Task 3.3 has not been started.
