# Storage foundation — Milestone 3, Task 3.1

Decision date: 2026-10-21. Foundation only: empty schema and initializer. CSV staging ingestion (Task 3.2), curated transformations, analytical SQL, exports and update automation are not implemented.

## Engine decision

Choose **SQLite only**, using Python's existing `sqlite3` module. The four preserved CSVs contain 176,004 records and total 14,759,016 bytes. The intended workload is local, one writer at a time, with reproducible snapshot loads and later SQL aggregations. No database server or additional Python dependency is needed. SQLite supports the local analysis/file-storage use case; Python provides its connection interface. [SQLite uses](https://www.sqlite.org/whentouse.html), [Python sqlite3 documentation](https://docs.python.org/3.11/library/sqlite3.html).

| Criterion | SQLite — selected | DuckDB — not introduced |
|---|---|---|
| Current size and workflow | Appropriate starting point for these modest local snapshots; transactions suit complete snapshot loads | Analytical capabilities are attractive, but this workload has not demonstrated a need for them |
| CSV preservation | Future Python CSV parsing will supply exact strings to explicit TEXT columns | Direct CSV scanning/type inference is convenient, but would still need deliberate lossless source handling |
| Analytical SQL | Later grouping, joins and window queries can serve the current research question | Column-oriented execution and file analytics may become valuable at larger scale |
| Setup | sqlite3 and SQLite 3.45.1 already work in the current Python environment | Would add another engine/library to the project |
| Power BI | Plan a later validated CSV export through Python, practical on Windows | CSV/Parquet export features are useful, but do not require choosing this engine now |

DuckDB is a credible analytical alternative, not an unsuitable product. Its additional capabilities do not currently offset another dependency or engine. No performance benchmark or Power BI integration test is claimed. Revisit only if actual query performance or file-analysis requirements warrant it. [DuckDB documentation](https://duckdb.org/docs/2.0/).

## Configuration and initialization

- Default database: `data/local/ttc.sqlite3`, relative to the project root regardless of working directory.
- Schema: `sql/storage_schema.sql`. Python entry point: `scripts/init_storage.py`.
- Override the database with `--database /absolute/path/example.sqlite3` (also accepts .sqlite/.db). Prefer the default ignored directory.
- Requires Python's sqlite3 with SQLite 3.38+ and JSON functions. STRICT tables retain declared types. Source fields remain TEXT even where values look numeric.
- Schema version is `PRAGMA user_version = 1`; application ID is `0x54544352` (TTCR). This is one explicit schema version, not a migration framework.

Run from the project root:

```sh
python3 scripts/init_storage.py
python3 scripts/init_storage.py
python3 -m unittest discover -s tests -v
```

Initialization creates definitions only, inside a transaction. It compares an existing database's application identity, version and complete schema definitions to the expected schema. A matching repeat preserves all rows; unrelated, changed or unsupported databases are rejected without repair or migration. Integrity and foreign-key checks run before commit. A failed fresh initialization can leave an empty database file, but no partial schema transaction is accepted.

The initializer enables foreign keys on its connection. **Every future ingestion connection must independently enable foreign keys before beginning a transaction**; the PRAGMA is connection-specific. No existing acquisition or profiling script opens this database.

## Structures and identity contracts

| Table | Grain / identity | Purpose |
|---|---|---|
| `raw_snapshots` | One resource/content pair; local `snapshot_id` primary key and UNIQUE `(resource_id, sha256)` | Package, CSV resource and related datastore IDs, source mode, hash, size and original header order as JSON |
| `retrieval_events` | One acquisition attempt, local `retrieval_id` | URL/final URL, start/end UTC timestamps, outcome, HTTP status/headers, raw location, original provenance path, failure message; successful attempts reference a snapshot |
| `staging_loads` | One successful committed staging receipt per snapshot | Parser version, completion time, raw/staged record counts and detailed reconciliation JSON |
| `staged_delay_records` | One source data record, PRIMARY KEY `(snapshot_id, record_ordinal)` | Eleven original columns as non-null TEXT, with exact names; blanks are empty strings |

No rows, source registry seeds, default snapshots, active-version selectors or curated tables are populated or created beyond these definitions. A staging receipt is separate from immutable snapshot metadata so a completed load can be recorded without changing what the source snapshot represents. Dictionary enrichment is deferred.

### Immutable snapshots and provenance

A snapshot identifies exact bytes for a particular CSV resource. SHA-256 is content identity, not incident identity; the same bytes under different resource IDs remain separately attributable. Snapshot IDs are local references, not portable source IDs. Mode is the source package mode, not inferred from route or vehicle labels.

Future registration must verify the existing raw file's size/hash against its provenance, preserve the original header order, and insert snapshot metadata once. Store paths relative to the project root for portability. Keep the existing dated provenance JSON unchanged: it already includes HTTP and verified-TLS/Python information, and remains the detailed acquisition audit record. The database stores the provenance reference plus retrieval fields; existing JSON files are not imported by initialization.

A repeated retrieval of the same resource/hash can add a retrieval event, but must reuse the snapshot and must not add another staged copy. Separate retrieval paths accommodate distinct timestamped copies of identical bytes. Failed acquisitions can have null HTTP status/headers and no snapshot reference; they are not zero-byte valid snapshots. Future provenance adaptation must explicitly handle legacy timestamp field names and retain the original JSON, rather than invent a source retrieval time.

Immutability is a workflow contract: do not update registered snapshot identity/metadata or overwrite/delete accepted raw files. The schema enforces content-pair uniqueness and valid modes/hash syntax/positive size, but does not prevent arbitrary external file edits or administrative UPDATE/DELETE. Future loading must rehash files and refuse mismatches. No new filesystem permissions or immutability triggers are introduced.

### Lossless records and traceability

Preserve `_id`, `Date`, `Time`, `Day`, `Station`, `Code`, `Min Delay`, `Min Gap`, `Bound`, `Line`, `Vehicle` exactly as decoded CSV strings. Do not trim, recase, coerce durations or replace blanks with SQL NULL. Keep zero-minute records, unknown codes, unusual labels, reported Day conflicts and duplicate candidates. Raw bytes remain authoritative for CSV quoting, newline and encoding details; staging is lossless at the decoded field-value level.

`record_ordinal` is one-based after the header and counts parsed CSV data records, not physical lines. Its identity is scoped to the immutable snapshot. Source `_id` is a TEXT attribute with **no unique constraint**; do not upsert or deduplicate incidents by `_id`, date/time, label combinations or a row fingerprint. Source row → snapshot → package/resource and retrieval/provenance provides traceability even when source IDs reset or change.

The database requires all eleven strings and a positive ordinal. Schema changes, malformed record widths or decode failures must be reported by the future loader and must not silently skip records. Changed schemas need an explicit compatibility decision. Current stored fields are not date/numeric interpretations; parsing rules and curated representations remain later tasks.

### Safe reruns, failures and future revisions

Task 3.2 must load all records and its staging receipt atomically. Before inserting anything, check for an already completed snapshot and validate its receipt; a repeat should be an explicit no-op/verification, not `INSERT OR IGNORE` that hides partial or mismatched records. The receipt's raw and staged counts must agree; schema CHECK constraints alone cannot compare them to the actual contents of another table. Parser-version changes must be an explicit rebuild/migration decision, not an automatic duplicate load.

A changed hash creates a new candidate snapshot; leave prior accepted data intact. Future current-mode outputs must deliberately select one validated snapshot per logical series, not union every historical export. Resource ID/URL replacements, narrower coverage and shrinking counts require investigation before treating a candidate as authoritative. No stable incident identity or append-only behavior is assumed. Active-snapshot selection/promotion and revision comparison are documented requirements, not implemented here; later tasks must add them before revised snapshots are published as current results.

## Reconciliation contract for Task 3.2

1. Verify bytes/hash and resource URL/ID against preserved provenance before parsing.
2. Validate exact column names, decode without lossy replacement, and retain every parsed source record and ordinal.
3. Compare independently counted raw records with inserted rows; ensure ordinal coverage 1..N, with no missing or repeated positions. Reconcile source values column-by-column where practical.
4. Record parser version, counts and checks in the staging receipt in the same transaction. Detailed reconciliation should include blank counts, source date coverage, valid recorded-minute totals, zero/invalid numeric counts and duplicate multiplicities. Any summaries are checks, not stored source transformations; do not combine Min Gap with Min Delay.
5. Compare existing profile results for the same content hash as a secondary check, not an ingestion dependency or a hardcoded forever-row-count assertion. Roll back on an unexplained mismatch.

These checks are not implemented ingestion. No CSV is read by the initializer or foundation tests.

## Git checkpoint and verification

Checkpoint commit: `dc22280` — completed source discovery, profiling and readiness evidence. It contains the 25 reviewed source/configuration/documentation/report/provenance files; no raw CSVs or local databases. Gitignore now also excludes environment files, credential/key locations and local working data. Public-source header cache IDs/ETags were reviewed as request metadata, not authentication credentials. Pattern scanning found no sensitive content. Git's whitespace check flagged five existing Markdown hard-break lines in source_assessment.md; those were deliberately preserved. No remote push occurred.

Task 3.1 foundation files are left uncommitted for review after this checkpoint. Commands executed: `git status`, candidate inventory/credential-pattern scan, `git check-ignore` probes, explicit `git add`, cached diff review and `git commit`; `python3 scripts/init_storage.py` twice; `python3 -m unittest discover -s tests -v`; final schema/count/raw-hash/file checks.

Observed results on Python 3.11.9 / SQLite 3.45.1: initialization succeeded twice, with all four table counts zero. Four tests passed: byte-preserving repeated initialization, rejection of an unrelated database, changed-schema rejection without repair, and unsupported-version rejection. Tests use temporary empty/synthetic-schema databases, with no staging inserts. Database integrity and foreign-key checks passed. The project database is ignored, as are raw snapshots and cache files.

## Unresolved questions

Min Gap semantics, trustworthy weekday interpretation (especially LRT), code-dictionary conflicts/omissions, recording thresholds, stable event identity and real revision behavior remain as documented in data_model_readiness.md. They do not prevent lossless staging, but do prevent automatic deduplication, semantic normalization and unqualified cross-mode comparisons. Physical storage does not resolve those analytical limitations.

Stop after Task 3.1. The next task is explicitly approved staging implementation, beginning with transactional reconciliation of the preserved Subway tracer, not concurrent work on curated outputs.
