-- All selected rows, including rows that cannot be allocated to the scoped period.
SELECT source_mode,COUNT(*) AS selected_records,
 SUM(incident_count_eligible) AS inventory_incidents,
 SUM(incident_count_eligible=1 AND scope_eligible=1) AS scoped_incidents,
 SUM(incident_count_eligible=1 AND scope_eligible=0) AS outside_or_unallocated_scope,
 SUM(scope_eligible=1 AND incident_count_eligible=1 AND scoped_hour_eligible=0) AS unallocated_hour,
 SUM(scope_eligible=1 AND incident_count_eligible=1 AND scoped_raw_line_eligible=0) AS excluded_raw_line,
 SUM(scope_eligible=1 AND incident_count_eligible=1 AND scoped_raw_code_eligible=0) AS excluded_raw_code,
 SUM(scope_eligible=1 AND incident_count_eligible=1 AND scoped_delay_minutes_eligible=0) AS ineligible_duration,
 SUM(scope_eligible=1 AND incident_count_eligible=1 AND scoped_raw_line_eligible=0 AND scoped_delay_minutes_eligible=1) AS excluded_line_duration_eligible,
 SUM(CASE WHEN scope_eligible=1 AND incident_count_eligible=1 AND scoped_raw_line_eligible=0 AND scoped_delay_minutes_eligible=1 THEN delay_minutes END) AS excluded_line_minutes,
 SUM(scope_eligible=1 AND incident_count_eligible=1 AND scoped_raw_code_eligible=0 AND scoped_delay_minutes_eligible=1) AS excluded_code_duration_eligible,
 SUM(CASE WHEN scope_eligible=1 AND incident_count_eligible=1 AND scoped_raw_code_eligible=0 AND scoped_delay_minutes_eligible=1 THEN delay_minutes END) AS excluded_code_minutes,
 SUM(date_status='missing') AS missing_date,SUM(date_status='invalid') AS invalid_date,
 SUM(time_status='missing') AS missing_time,SUM(time_status='invalid') AS invalid_time,
 SUM(delay_status='missing') AS missing_delay,SUM(delay_status='invalid') AS invalid_delay,
 SUM(delay_minutes<0) AS negative_delay_records,
 SUM(validated_weekday_eligible) AS validated_weekday_records
FROM curated_records GROUP BY source_mode ORDER BY source_mode;
