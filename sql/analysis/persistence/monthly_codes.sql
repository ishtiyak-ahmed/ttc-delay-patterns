-- Read-only. One disjoint category per scoped source record, including ineligible/missing bucket.
-- NULL category_raw plus category_eligible=0 denotes a bucket, never an invented raw label.
WITH base AS (
 SELECT *,substr(parsed_date,1,7) AS month,
 scoped_raw_code_eligible AS category_eligible,
 CASE WHEN scoped_raw_code_eligible=1 THEN code_raw END AS category_raw
 FROM curated_records WHERE incident_count_eligible=1 AND scope_eligible=1
), mode_month AS (
 SELECT source_mode,month,COUNT(*) AS mode_month_incidents,
 SUM(scoped_delay_minutes_eligible) AS mode_month_duration_eligible,
 SUM(CASE WHEN scoped_delay_minutes_eligible=1 THEN delay_minutes END) AS mode_month_minutes,
 COUNT(DISTINCT parsed_date) AS mode_month_observed_dates,
 MIN(parsed_date) AS mode_month_first_date,MAX(parsed_date) AS mode_month_last_date,
 CAST(strftime('%d',date(month||'-01','+1 month','-1 day')) AS INTEGER) AS calendar_month_days,
 SUM(category_eligible=0) AS mode_month_missing_category_incidents,
 SUM(CASE WHEN category_eligible=0 AND scoped_delay_minutes_eligible=1 THEN delay_minutes END) AS mode_month_missing_category_minutes
 FROM base GROUP BY source_mode,month
), categories AS (
 SELECT source_mode,month,category_eligible,category_raw,
 COUNT(*) AS recorded_incidents,
 SUM(scoped_delay_minutes_eligible) AS duration_eligible_incidents,
 SUM(scoped_delay_minutes_eligible=0) AS duration_ineligible_incidents,
 SUM(CASE WHEN scoped_delay_minutes_eligible=1 THEN delay_minutes END) AS recorded_delay_minutes,
 SUM(CASE WHEN scoped_delay_minutes_eligible=1 AND delay_minutes=0 THEN 1 ELSE 0 END) AS zero_minute_incidents,
 COUNT(DISTINCT parsed_date) AS category_observed_dates,
 MIN(parsed_date) AS category_first_date,MAX(parsed_date) AS category_last_date,
 SUM(CASE WHEN scoped_delay_minutes_eligible=1 AND delay_minutes>60 THEN 1 ELSE 0 END) AS over60_incidents,
 SUM(CASE WHEN scoped_delay_minutes_eligible=1 AND delay_minutes>60 THEN delay_minutes END) AS over60_minutes,
 SUM(CASE WHEN scoped_delay_minutes_eligible=1 AND delay_minutes>120 THEN 1 ELSE 0 END) AS over120_incidents,
 SUM(CASE WHEN scoped_delay_minutes_eligible=1 AND delay_minutes>120 THEN delay_minutes END) AS over120_minutes,
 SUM(duplicate_candidate) AS duplicate_candidate_incidents,
 SUM(CASE WHEN duplicate_candidate=1 AND scoped_delay_minutes_eligible=1 THEN delay_minutes END) AS duplicate_candidate_minutes
 FROM base GROUP BY source_mode,month,category_eligible,category_raw
), ranks AS (
 SELECT source_mode,month,category_raw,
 RANK() OVER(PARTITION BY source_mode,month ORDER BY recorded_incidents DESC) AS incident_rank,
 CASE WHEN recorded_delay_minutes IS NOT NULL THEN RANK() OVER(PARTITION BY source_mode,month ORDER BY recorded_delay_minutes DESC) END AS minute_rank
 FROM categories WHERE category_eligible=1
)
SELECT c.*,m.mode_month_incidents,m.mode_month_duration_eligible,m.mode_month_minutes,
 m.mode_month_observed_dates,m.mode_month_first_date,m.mode_month_last_date,m.calendar_month_days,
 m.mode_month_missing_category_incidents,m.mode_month_missing_category_minutes,
 1.0*c.recorded_incidents/m.mode_month_incidents AS share_monthly_mode_incidents,
 1.0*c.recorded_delay_minutes/NULLIF(m.mode_month_minutes,0) AS share_monthly_mode_minutes,
 r.incident_rank,r.minute_rank
FROM categories c JOIN mode_month m USING(source_mode,month)
LEFT JOIN ranks r ON r.source_mode=c.source_mode AND r.month=c.month AND r.category_raw=c.category_raw AND c.category_eligible=1
ORDER BY c.source_mode,c.month,c.category_eligible DESC,c.category_raw;
