-- Read-only; scoped recorded rows, exact raw labels, eligible durations only.
WITH base AS (SELECT *, CASE WHEN scoped_delay_minutes_eligible=0 THEN 'unavailable_or_ineligible' WHEN delay_minutes=0 THEN 'zero' WHEN delay_minutes<=5 THEN 'positive_0_to_5' WHEN delay_minutes<=15 THEN 'over_5_to_15' WHEN delay_minutes<=30 THEN 'over_15_to_30' WHEN delay_minutes<=60 THEN 'over_30_to_60' WHEN delay_minutes<=120 THEN 'over_60_to_120' ELSE 'over_120' END AS duration_band FROM curated_records WHERE incident_count_eligible=1 AND scope_eligible=1),
ordered AS (
 SELECT source_mode, duration_band, delay_minutes,
 ROW_NUMBER() OVER (PARTITION BY source_mode, duration_band ORDER BY delay_minutes,snapshot_id,record_ordinal) AS rn,
 COUNT(*) OVER (PARTITION BY source_mode, duration_band) AS n
 FROM base WHERE scoped_delay_minutes_eligible=1
), medians AS (
 SELECT source_mode, duration_band, AVG(delay_minutes) AS median_recorded_minutes
 FROM ordered WHERE rn IN ((n+1)/2,(n+2)/2) GROUP BY source_mode, duration_band
), aggregates AS (
 SELECT source_mode, duration_band, COUNT(*) AS recorded_incidents,
 SUM(scoped_delay_minutes_eligible) AS duration_eligible_incidents,
 SUM(CASE WHEN scoped_delay_minutes_eligible=1 THEN delay_minutes END) AS recorded_delay_minutes,
 AVG(CASE WHEN scoped_delay_minutes_eligible=1 THEN delay_minutes END) AS average_recorded_minutes,
 SUM(CASE WHEN scoped_delay_minutes_eligible=1 AND delay_minutes=0 THEN 1 ELSE 0 END) AS zero_minute_incidents,
 SUM(CASE WHEN scoped_delay_minutes_eligible=1 AND delay_minutes>0 THEN 1 ELSE 0 END) AS positive_minute_incidents,
 SUM(scoped_delay_minutes_eligible=0) AS duration_ineligible_incidents,
 COUNT(DISTINCT parsed_date) AS observed_dates,
 SUM(weekday_conflict=1) AS weekday_conflicts,
 SUM(duplicate_candidate) AS duplicate_candidate_records
 FROM base GROUP BY source_mode, duration_band
)
SELECT a.*,m.median_recorded_minutes,
 1.0*a.zero_minute_incidents/NULLIF(a.duration_eligible_incidents,0) AS zero_minute_share
FROM aggregates a LEFT JOIN medians m ON a.source_mode IS m.source_mode AND a.duration_band IS m.duration_band
ORDER BY a.source_mode, a.duration_band;
