-- Calendar span is coverage context, never an exposure or service denominator.
SELECT source_mode,MIN(parsed_date) AS first_observed_date,MAX(parsed_date) AS last_observed_date,
 COUNT(DISTINCT parsed_date) AS observed_dates,
 CAST(julianday(MAX(parsed_date))-julianday(MIN(parsed_date))+1 AS INTEGER) AS calendar_span_days,
 CAST(julianday(MAX(parsed_date))-julianday(MIN(parsed_date))+1 AS INTEGER)-COUNT(DISTINCT parsed_date) AS dates_without_records_within_span,
 COUNT(DISTINCT substr(parsed_date,1,7)) AS observed_months
FROM curated_records WHERE incident_count_eligible=1 AND scope_eligible=1
GROUP BY source_mode ORDER BY source_mode;
