# Repeat-safe staging and snapshot versioning — Task 3.3

Completed 2026-10-21. This extends the existing staging workflow without changing schema v1, parsing, source values or incident semantics. No curated/current dataset, analytical query, scheduling or downloads were introduced.

## Audit before editing

The existing foundation already provided:

- UNIQUE `(resource_id, sha256)` for immutable source content and `(snapshot_id, record_ordinal)` for staged rows. `_id` is only a source TEXT field.
- Verification of an identical previously staged snapshot against raw bytes, every source field, reconciliation receipt and selected provenance; no replacement or ignore-insert logic.
- Separate snapshot IDs for revised contents under the same CKAN resource; earlier rows can remain alongside later rows. The original data already have four snapshots and 176,004 records.
- One `BEGIN IMMEDIATE` transaction covering snapshot registration, provenance, rows and successful receipt. Exceptions roll back the snapshot; earlier completed snapshots remain.

Missing evidence: revision/coexistence, interrupted-load retry and row-reordering tests. Missing functionality: a separately preserved retrieval of identical bytes was rejected, and the independent verifier assumed one retrieval per snapshot. No trustworthy source-version precedence was documented.

## Targeted changes

`register_retrieval` in `scripts/ingest_staging.py` now distinguishes a provenance event from content identity. It verifies existing metadata for the selected immutable provenance path or records that new retrieval once. Reusing a provenance path for different metadata/content is rejected, never rebound. The loader's `BEGIN IMMEDIATE` serializes event lookup/insert; no schema migration or new index is needed for this local writer workflow. The schema itself does not prohibit duplicate provenance paths introduced through arbitrary external SQL; loader and verifier reject such ambiguity instead of repairing it.

The independent verifier now validates every successful retrieval for each snapshot against its preserved raw/provenance, while comparing staged rows once per snapshot. It does not multiply row counts by retrieval-event counts. Its reported total covers **all stored versions**, not a current analytical dataset.

Repeated provenance paths in one CLI invocation are individually recognized, but summary totals count unique selected snapshot IDs once. The summary explicitly describes its scope as selected stored versions, not current incidents.

The parser version remains unchanged because field decoding, mapping and reconciliation semantics did not change. Existing receipts and snapshots are preserved.

| Input/state | Result |
|---|---|
| Same resource/hash, same recorded provenance | `verified_existing`; no new snapshot, rows, receipt or retrieval. Existing metadata and data must reconcile. |
| Same resource/hash, separately preserved provenance path | Verify existing content/receipt, register one additional retrieval, retain the same snapshot and staged rows. Repeating it adds no more events. |
| Different hash, same resource | Register a distinct snapshot/receipt and its source rows. Preserve previous versions; no incident-level merge or automatic promotion. |
| Changed row order or CSV representation | Different bytes can mean a new content snapshot. This is not evidence of new real-world incidents. |
| Reused `_id` across versions | Allowed; identity remains snapshot plus record ordinal. No upsert based on source IDs. |
| Incompatible metadata/parser receipt, incomplete externally created state or duplicate provenance events | Fail clearly; do not overwrite, repair or silently skip the inconsistency. |
| `--verify-only` with an unregistered provenance event | Reject; verification cannot register a new retrieval. |

No staged record or snapshot is updated/deleted by ingestion. A provenance event may be added only after the selected input validates, and is rolled back if any later reconciliation or source-file stability check fails. Different snapshots are retained independently; no code combines their contents into a single current dataset.

## Recovery policy and tested limits

For a new snapshot, registration, event insertion, staged records, reconciliation and receipt commit atomically. A normal exception or malformed later record rolls back earlier inserts in that transaction. A failure in a later member of a multi-snapshot CLI invocation does not roll back earlier committed snapshots. Repeating the explicit input list verifies completed members and retries uncommitted members. The database receipts remain authoritative if a process commits but exits before writing its combined JSON report; a rerun must use a new report path because reports refuse overwrite.

Recovery tests use only temporary synthetic fixtures:

- Inject an exception when the parser asks for record 2, after record 1 was inserted. Verify the previous version and all counts remain unchanged; retry the same revised input successfully.
- Run the loader in a subprocess that calls `os._exit(73)` at that same point, bypassing Python rollback/finally. Reopen SQLite, confirm no partial snapshot/event/receipt/rows remain, and retry successfully. The earlier snapshot is still exact.
- Retain existing tests for malformed CSV and failure after inserts during reconciliation.

This simulates application/process interruption and SQLite reopening, not OS power failure, disk corruption, a full disk or broken hardware. Those scenarios were not tested. SQLite cannot protect against someone editing accepted raw/provenance files or manually altering database tables. Partial state created outside the transaction is rejected for review rather than auto-deleted. Raw/provenance files are checked before load and again before commit but not filesystem-locked. Parser-version changes still require an explicit rebuild/migration decision.

No persistent failed-load journal was added: rejected attempts raise an error; they do not leave partial success metadata. Successful acquisition events remain separate from load attempts. Original failed network-acquisition provenance remains untouched.

## Explicit analytical snapshot selection policy

**There is no automatic “current” snapshot.** All stored versions are an audit history. Ingestion success means the selected bytes were staged losslessly, not that they are the publisher's authoritative latest data.

| Concept | Meaning | What it does not establish |
|---|---|---|
| Source publication metadata | Catalog refresh fields, response Last-Modified/ETag and any explicit publisher revision information | A reliable monotonic revision number, complete history or precedence over another candidate |
| Retrieval timestamp | When this acquisition observed the bytes; more than one retrieval may reference one snapshot | Publication time, recency of the actual contents or authority |
| Content checksum | SHA-256 of exact bytes | Time ordering, semantic equivalence or incident identity |
| Snapshot identity | Local snapshot_id tied to resource_id plus checksum | A stable TTC event ID or automatic analytical inclusion |
| Analytical selection | An explicit approved mapping from logical source/resource to a reconciled snapshot and checksum, recorded for each output | Permission to union all historical versions or select MAX(timestamp) |

Before a future analytical layer uses data, explicitly choose **one approved snapshot per logical resource/series**, recording resource ID, snapshot ID, checksum and the rationale for that selection. Check complete receipt, provenance, schema compatibility, coverage and unexplained shrinkage/corrections first. Preserve the mapping with the resulting output so a later retrieval does not silently change its evidence. Resolve the mapping by identity and checksum, not just a local numeric ID.

Do not default to the most recently ingested or retrieved snapshot. Source Last-Modified or higher row counts are also insufficient by themselves. A rolling window, corrected history, cache lag or reordered export could otherwise be misinterpreted. A replacement CKAN resource ID requires an explicit same-series decision before selecting one version; never automatically include both as independent incident sets.

For this task's verification, the four **original** snapshot IDs 1–4 were explicitly selected by their preserved provenance paths. No authority claim or future analytical selection is inferred from those numeric IDs. No selector table, current-data view or curated transformation is implemented here.

## Files changed and verification

Modified existing files:

- `scripts/ingest_staging.py`: retrieval-event verification/registration, keeping original transaction and staging logic.
- `scripts/verify_staging.py`: verify multiple retrievals per snapshot without duplicate counting.
- `tests/test_staging_ingestion.py`: extract the existing fixture base and allow named synthetic files; the original 12 tests retain their assertions.

Created:

- `tests/test_snapshot_versioning.py`: eleven new offline tests for normal reruns, revised/shrunken content under the same resource, coexistence and provenance, reordering, additional retrieval idempotence, verify-only protection, exception/retry, abrupt process exit/retry, checksum rejection after prior success, reused-provenance rejection and refusal to repair external partial state. Some tests cover multiple related requirements.
- `docs/snapshot_versioning.md`: this audit, contracts, recovery limits and explicit selection policy.
- `reports/repeat_ingestion_results.json`: actual four-snapshot normal rerun results.
- `reports/repeat_verification_results.json`: actual independent raw-to-database reconciliation results.

Commands executed:

```sh
python3 -m unittest discover -s tests -v
python3 scripts/ingest_staging.py --provenance \
  data/provenance/20261021T190204614685Z__subway.json \
  data/provenance/20261021T190548363172Z__bus.json \
  data/provenance/20261021T190549738480Z__streetcar.json \
  data/provenance/20261021T190550293696Z__lrt.json \
  --report reports/repeat_ingestion_results.json
python3 scripts/verify_staging.py --report reports/repeat_verification_results.json
```

Additional checks read schema constraints, provenance inventory, counts and pre-task SHA-256 file inventories. All 27 tests passed (11 new, 12 original staging, four foundation). Real-data reruns returned `verified_existing` for every mode and `retrieval_registered: false`. They created no additional snapshots/events/receipts/staged records.

| Mode | Original snapshot | Rows before | Rows after |
|---|---:|---:|---:|
| Subway | 1 | 45,475 | 45,475 |
| Bus | 2 | 102,257 | 102,257 |
| Streetcar | 3 | 23,703 | 23,703 |
| LRT | 4 | 4,569 | 4,569 |
| Total | — | 176,004 | 176,004 |

Independent verification again compared 1,936,044 exact field values and traced all 176,004 rows to preserved provenance. Integrity check: `ok`; foreign-key violations: zero. Raw snapshot checksums match both prior records and provenance. The **entire real database file remained byte-for-byte identical** to its pre-task SHA-256: rows, metadata and original receipts were not rewritten. All new revision/retrieval/interruption cases ran only in disposable fixtures.

The SQL schema, initializer, original raw files, provenance, governing documents, discovery metadata, profiling results and Task 3.2 result artifacts remain unchanged. No data was downloaded, dependencies added, commits made or pushes performed. Actual City publication/revision behavior and source semantics remain uncertain; synthetic tests establish local storage behavior only. Stop after Task 3.3 for review; Milestone 4 was not started.
