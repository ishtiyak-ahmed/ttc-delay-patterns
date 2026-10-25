-- Read-only; scoped recorded rows, exact raw labels, eligible durations only.
WITH base AS (SELECT * FROM curated_records WHERE incident_count_eligible=1 AND scope_eligible=1 AND scoped_hour_eligible=1),
ordered AS (
 SELECT source_mode, hour_of_day, delay_minutes,
 ROW_NUMBER() OVER (PARTITION BY source_mode, hour_of_day ORDER BY delay_minutes,snapshot_id,record_ordinal) AS rn,
 COUNT(*) OVER (PARTITION BY source_mode, hour_of_day) AS n
 FROM base WHERE scoped_delay_minutes_eligible=1
), medians AS (
 SELECT source_mode, hour_of_day, AVG(delay_minutes) AS median_recorded_minutes
 FROM ordered WHERE rn IN ((n+1)/2,(n+2)/2) GROUP BY source_mode, hour_of_day
), aggregates AS (
 SELECT source_mode, hour_of_day, COUNT(*) AS recorded_incidents,
 SUM(scoped_delay_minutes_eligible) AS duration_eligible_incidents,
 SUM(CASE WHEN scoped_delay_minutes_eligible=1 THEN delay_minutes END) AS recorded_delay_minutes,
 AVG(CASE WHEN scoped_delay_minutes_eligible=1 THEN delay_minutes END) AS average_recorded_minutes,
 SUM(CASE WHEN scoped_delay_minutes_eligible=1 AND delay_minutes=0 THEN 1 ELSE 0 END) AS zero_minute_incidents,
 SUM(CASE WHEN scoped_delay_minutes_eligible=1 AND delay_minutes>0 THEN 1 ELSE 0 END) AS positive_minute_incidents,
 SUM(scoped_delay_minutes_eligible=0) AS duration_ineligible_incidents,
 COUNT(DISTINCT parsed_date) AS observed_dates,
 SUM(weekday_conflict=1) AS weekday_conflicts,
 SUM(duplicate_candidate) AS duplicate_candidate_records
 FROM base GROUP BY source_mode, hour_of_day
)
SELECT a.*,m.median_recorded_minutes,
 1.0*a.zero_minute_incidents/NULLIF(a.duration_eligible_incidents,0) AS zero_minute_share
FROM aggregates a LEFT JOIN medians m ON a.source_mode IS m.source_mode AND a.hour_of_day IS m.hour_of_day
ORDER BY a.source_mode, a.hour_of_day;
