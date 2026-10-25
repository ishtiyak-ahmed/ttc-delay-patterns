-- Absence of records is NOT evidence of zero-delay service. Only internal gaps.
WITH RECURSIVE bounds AS (
 SELECT source_mode,MIN(parsed_date) AS first_date,MAX(parsed_date) AS last_date
 FROM curated_records WHERE incident_count_eligible=1 AND scope_eligible=1 GROUP BY source_mode
), calendar(source_mode,calendar_date,last_date) AS (
 SELECT source_mode,first_date,last_date FROM bounds
 UNION ALL SELECT source_mode,date(calendar_date,'+1 day'),last_date FROM calendar WHERE calendar_date<last_date
), observed AS (
 SELECT DISTINCT source_mode,parsed_date FROM curated_records WHERE incident_count_eligible=1 AND scope_eligible=1
)
SELECT c.source_mode,c.calendar_date FROM calendar c LEFT JOIN observed o
ON o.source_mode=c.source_mode AND o.parsed_date=c.calendar_date
WHERE o.parsed_date IS NULL ORDER BY c.source_mode,c.calendar_date;
