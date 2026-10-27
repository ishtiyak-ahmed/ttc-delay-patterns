// Paste EACH named block into its own Blank Query / Advanced Editor. Not one combined query.
// ExportFolder is a Text parameter containing the Windows folder path, without trailing slash.
// Load only the ten tables. Disable load for ReadTtcCsv. No trimming or blank-to-zero replacements.

// QUERY: ReadTtcCsv (function, Disable Enable Load)
(fileName as text, fieldTypes as list) as table =>
let
    Raw = Csv.Document(File.Contents(ExportFolder & "\" & fileName), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Raw, [PromoteAllScalars=true]),
    Expected = List.Transform(fieldTypes, each _{0}),
    Checked = if Table.ColumnNames(Headers) = Expected then Headers else error "CSV schema differs from verified contract",
    // Blank text numeric/date cells become null only in typed columns; raw text is untouched.
    Typed = List.Accumulate(fieldTypes, Checked, (current, pair) =>
        Table.TransformColumns(current, {{pair{0}, (v) =>
            if pair{1} = type text then v
            else if v = null or v = "" then null
            else if pair{1} = type date then Date.FromText(v, [Format="yyyy-MM-dd", Culture="en-US"])
            else if pair{0} = "recorded_delay_minutes" then Number.FromText(v, "en-US")
            else let n = Number.FromText(v, "en-US")
                 in if Number.RoundTowardZero(n) = n then Int64.From(n)
                    else error "Noninteger value in a count/flag column", pair{1}}}))
in Typed

// QUERY: DimMode
ReadTtcCsv("dim_mode.csv", {
    {"source_mode", type text},
    {"snapshot_id", Int64.Type},
    {"resource_id", type text},
    {"raw_sha256", type text},
    {"first_observed_date", type date},
    {"last_observed_date", type date},
    {"observed_dates", Int64.Type},
    {"calendar_span_days", Int64.Type},
    {"dates_without_records_within_span", Int64.Type},
    {"observed_months", Int64.Type},
    {"selected_records", Int64.Type},
    {"outside_or_unallocated_scope", Int64.Type},
    {"missing_date", Int64.Type},
    {"invalid_date", Int64.Type},
    {"missing_time", Int64.Type},
    {"invalid_time", Int64.Type},
    {"missing_delay", Int64.Type},
    {"invalid_delay", Int64.Type},
    {"negative_delay_records", Int64.Type},
    {"validated_weekday_records", Int64.Type}
})

// QUERY: DimMonth
ReadTtcCsv("dim_month.csv", {
    {"month_start", type date},
    {"month_label", type text},
    {"year", Int64.Type},
    {"month_number", Int64.Type}
})

// QUERY: DimCode
ReadTtcCsv("dim_code.csv", {
    {"code_key", type text},
    {"source_mode", type text},
    {"category_eligible", Int64.Type},
    {"raw_code", type text},
    {"code_description", type text},
    {"code_display_label", type text}
})

// QUERY: DimLine
ReadTtcCsv("dim_line.csv", {
    {"line_key", type text},
    {"source_mode", type text},
    {"category_eligible", Int64.Type},
    {"raw_line", type text}
})

// QUERY: DimDurationBand
ReadTtcCsv("dim_duration_band.csv", {
    {"duration_band", type text},
    {"sort_order", Int64.Type},
    {"is_over60", Int64.Type},
    {"is_zero", Int64.Type},
    {"is_duration_eligible", Int64.Type}
})

// QUERY: FactMonth
ReadTtcCsv("fact_month.csv", {
    {"source_mode", type text},
    {"month_start", type date},
    {"recorded_incidents", Int64.Type},
    {"duration_eligible_incidents", Int64.Type},
    {"duration_ineligible_incidents", Int64.Type},
    {"recorded_delay_minutes", type number},
    {"zero_minute_incidents", Int64.Type},
    {"observed_dates", Int64.Type},
    {"weekday_conflicts", Int64.Type},
    {"duplicate_candidate_records", Int64.Type},
    {"first_observed_date", type date},
    {"last_observed_date", type date},
    {"calendar_month_days", Int64.Type},
    {"missing_code_incidents", Int64.Type},
    {"missing_line_incidents", Int64.Type}
})

// QUERY: FactCode
ReadTtcCsv("fact_code.csv", {
    {"source_mode", type text},
    {"month_start", type date},
    {"code_key", type text},
    {"recorded_incidents", Int64.Type},
    {"duration_eligible_incidents", Int64.Type},
    {"duration_ineligible_incidents", Int64.Type},
    {"recorded_delay_minutes", type number},
    {"zero_minute_incidents", Int64.Type},
    {"category_observed_dates", Int64.Type},
    {"category_first_date", type date},
    {"category_last_date", type date}
})

// QUERY: FactLine
ReadTtcCsv("fact_line.csv", {
    {"source_mode", type text},
    {"month_start", type date},
    {"line_key", type text},
    {"recorded_incidents", Int64.Type},
    {"duration_eligible_incidents", Int64.Type},
    {"duration_ineligible_incidents", Int64.Type},
    {"recorded_delay_minutes", type number},
    {"zero_minute_incidents", Int64.Type},
    {"category_observed_dates", Int64.Type},
    {"category_first_date", type date},
    {"category_last_date", type date}
})

// QUERY: FactDuration
ReadTtcCsv("fact_duration.csv", {
    {"source_mode", type text},
    {"month_start", type date},
    {"duration_band", type text},
    {"is_bus_mfdv", Int64.Type},
    {"recorded_incidents", Int64.Type},
    {"duration_eligible_incidents", Int64.Type},
    {"duration_ineligible_incidents", Int64.Type},
    {"recorded_delay_minutes", type number},
    {"zero_minute_incidents", Int64.Type}
})

// QUERY: ReportingGaps
ReadTtcCsv("reporting_gaps.csv", {
    {"source_mode", type text},
    {"month_start", type date},
    {"calendar_date", type date}
})
