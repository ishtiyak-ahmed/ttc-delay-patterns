-- Storage schema v1. Definitions only: no source or staging rows are inserted.
CREATE TABLE raw_snapshots (
    snapshot_id INTEGER PRIMARY KEY,
    package_id TEXT NOT NULL,
    resource_id TEXT NOT NULL,
    datastore_resource_id TEXT NOT NULL,
    source_mode TEXT NOT NULL CHECK (source_mode IN ('subway', 'bus', 'streetcar', 'lrt')),
    sha256 TEXT NOT NULL CHECK (length(sha256) = 64 AND sha256 NOT GLOB '*[^0-9a-f]*'),
    file_size_bytes INTEGER NOT NULL CHECK (file_size_bytes > 0),
    original_columns_json TEXT NOT NULL CHECK (json_valid(original_columns_json)),
    UNIQUE (resource_id, sha256)
) STRICT;

-- Retrievals are separate from content identity, including repeated/failed attempts.
CREATE TABLE retrieval_events (
    retrieval_id INTEGER PRIMARY KEY,
    snapshot_id INTEGER REFERENCES raw_snapshots(snapshot_id),
    resource_id TEXT NOT NULL,
    source_url TEXT NOT NULL,
    final_url TEXT,
    started_at_utc TEXT NOT NULL,
    finished_at_utc TEXT NOT NULL,
    outcome TEXT NOT NULL CHECK (outcome IN ('downloaded', 'failed')),
    http_status INTEGER CHECK (http_status BETWEEN 100 AND 599),
    response_headers_json TEXT CHECK (response_headers_json IS NULL OR json_valid(response_headers_json)),
    raw_path TEXT,
    provenance_path TEXT NOT NULL,
    error_message TEXT,
    CHECK (
        (outcome = 'downloaded' AND snapshot_id IS NOT NULL AND http_status IS NOT NULL
         AND http_status = 200 AND raw_path IS NOT NULL AND error_message IS NULL)
        OR (outcome = 'failed' AND snapshot_id IS NULL AND error_message IS NOT NULL)
    )
) STRICT;

-- A successful staging receipt is committed with its rows in a future task.
CREATE TABLE staging_loads (
    snapshot_id INTEGER PRIMARY KEY REFERENCES raw_snapshots(snapshot_id),
    parser_version TEXT NOT NULL,
    completed_at_utc TEXT NOT NULL,
    raw_record_count INTEGER NOT NULL CHECK (raw_record_count >= 0),
    staged_record_count INTEGER NOT NULL CHECK (staged_record_count = raw_record_count),
    reconciliation_json TEXT NOT NULL CHECK (json_valid(reconciliation_json))
) STRICT;

-- All original CSV values are TEXT. Empty strings and repeated records are retained.
CREATE TABLE staged_delay_records (
    snapshot_id INTEGER NOT NULL REFERENCES raw_snapshots(snapshot_id),
    record_ordinal INTEGER NOT NULL CHECK (record_ordinal > 0),
    "_id" TEXT NOT NULL,
    "Date" TEXT NOT NULL,
    "Time" TEXT NOT NULL,
    "Day" TEXT NOT NULL,
    "Station" TEXT NOT NULL,
    "Code" TEXT NOT NULL,
    "Min Delay" TEXT NOT NULL,
    "Min Gap" TEXT NOT NULL,
    "Bound" TEXT NOT NULL,
    "Line" TEXT NOT NULL,
    "Vehicle" TEXT NOT NULL,
    PRIMARY KEY (snapshot_id, record_ordinal)
) STRICT;
