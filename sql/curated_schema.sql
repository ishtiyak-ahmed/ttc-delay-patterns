CREATE TABLE curated_metadata (
    singleton INTEGER PRIMARY KEY CHECK (singleton=1),
    rule_version TEXT NOT NULL,
    selection_json TEXT NOT NULL CHECK(json_valid(selection_json)),
    specification_sha256 TEXT NOT NULL,
    implementation_sha256 TEXT NOT NULL
) STRICT;
CREATE TABLE curated_selection (
    snapshot_id INTEGER PRIMARY KEY,
    source_mode TEXT NOT NULL UNIQUE,
    resource_id TEXT NOT NULL UNIQUE,
    sha256 TEXT NOT NULL,
    staged_record_count INTEGER NOT NULL
) STRICT;
CREATE TABLE curated_records (
    snapshot_id INTEGER NOT NULL REFERENCES curated_selection(snapshot_id),
    record_ordinal INTEGER NOT NULL,
    source_mode TEXT NOT NULL,
    source_id TEXT NOT NULL, date_raw TEXT NOT NULL, time_raw TEXT NOT NULL,
    day_raw TEXT NOT NULL, station_raw TEXT NOT NULL, code_raw TEXT NOT NULL,
    min_delay_raw TEXT NOT NULL, min_gap_raw TEXT NOT NULL,
    bound_raw TEXT NOT NULL, line_raw TEXT NOT NULL, vehicle_raw TEXT NOT NULL,
    parsed_date TEXT, parsed_time TEXT, hour_of_day INTEGER, derived_weekday TEXT,
    date_status TEXT NOT NULL, time_status TEXT NOT NULL, day_status TEXT NOT NULL,
    weekday_conflict INTEGER, bus_date_nonmidnight INTEGER NOT NULL,
    delay_minutes ANY, gap_value ANY,
    delay_status TEXT NOT NULL, gap_status TEXT NOT NULL,
    gap_semantic_status TEXT NOT NULL,
    delay_gt60 INTEGER, delay_gt120 INTEGER, delay_gt1440 INTEGER,
    gap_less_than_delay INTEGER,
    duplicate_group_size INTEGER NOT NULL, duplicate_candidate INTEGER NOT NULL,
    station_missing INTEGER NOT NULL, line_missing INTEGER NOT NULL,
    bound_missing INTEGER NOT NULL, bound_noncardinal INTEGER NOT NULL,
    vehicle_missing INTEGER NOT NULL, vehicle_zero_candidate INTEGER NOT NULL,
    line_has_slash INTEGER NOT NULL, station_length22_candidate INTEGER NOT NULL,
    code_status TEXT NOT NULL, code_description TEXT,
    incident_count_eligible INTEGER NOT NULL, scope_eligible INTEGER NOT NULL,
    delay_minutes_eligible INTEGER NOT NULL, scoped_delay_minutes_eligible INTEGER NOT NULL,
    hour_eligible INTEGER NOT NULL, scoped_hour_eligible INTEGER NOT NULL,
    raw_line_eligible INTEGER NOT NULL, scoped_raw_line_eligible INTEGER NOT NULL,
    raw_code_eligible INTEGER NOT NULL, scoped_raw_code_eligible INTEGER NOT NULL,
    description_eligible INTEGER NOT NULL, canonical_route_eligible INTEGER NOT NULL,
    weekday_exploratory_eligible INTEGER NOT NULL,
    weekday_conflict_excluded_eligible INTEGER NOT NULL,
    validated_weekday_eligible INTEGER NOT NULL,
    PRIMARY KEY(snapshot_id,record_ordinal),
    CHECK(delay_minutes IS NULL OR typeof(delay_minutes) IN ('integer','real')),
    CHECK(gap_value IS NULL OR typeof(gap_value) IN ('integer','real'))
) STRICT;
