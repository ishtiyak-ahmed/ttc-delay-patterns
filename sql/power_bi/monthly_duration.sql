-- One disjoint duration band and literal Bus-MFDV membership per selected scoped record.
-- >60 and MFDV overlap is a subset of this partition, never an extra population to append.
WITH base AS (
 SELECT *,substr(parsed_date,1,7)||'-01' AS month_start,
 CASE WHEN source_mode='bus' AND code_raw='MFDV' THEN 1 ELSE 0 END AS is_bus_mfdv,
 CASE WHEN scoped_delay_minutes_eligible=0 THEN 'unavailable_or_ineligible'
 WHEN delay_minutes=0 THEN 'zero' WHEN delay_minutes<=5 THEN 'positive_0_to_5'
 WHEN delay_minutes<=15 THEN 'over_5_to_15' WHEN delay_minutes<=30 THEN 'over_15_to_30'
 WHEN delay_minutes<=60 THEN 'over_30_to_60' WHEN delay_minutes<=120 THEN 'over_60_to_120'
 ELSE 'over_120' END AS duration_band
 FROM curated_records WHERE incident_count_eligible=1 AND scope_eligible=1
)
SELECT source_mode,month_start,duration_band,is_bus_mfdv,
 COUNT(*) AS recorded_incidents,
 SUM(scoped_delay_minutes_eligible) AS duration_eligible_incidents,
 SUM(scoped_delay_minutes_eligible=0) AS duration_ineligible_incidents,
 SUM(CASE WHEN scoped_delay_minutes_eligible=1 THEN delay_minutes END) AS recorded_delay_minutes,
 SUM(CASE WHEN scoped_delay_minutes_eligible=1 AND delay_minutes=0 THEN 1 ELSE 0 END) AS zero_minute_incidents
FROM base GROUP BY source_mode,month_start,duration_band,is_bus_mfdv
ORDER BY source_mode,month_start,duration_band,is_bus_mfdv;
