INSERT INTO curated_records
WITH parsed AS MATERIALIZED (
    SELECT d.*, s.source_mode,
           strict_date(s.source_mode,d."Date") AS parsed_date,
           strict_time(d."Time") AS parsed_time,
           strict_number(d."Min Delay") AS delay_minutes,
           strict_number(d."Min Gap") AS gap_value,
           COUNT(*) OVER (PARTITION BY d.snapshot_id,d."Date",d."Time",d."Day",
             d."Station",d."Code",d."Min Delay",d."Min Gap",d."Bound",d."Line",d."Vehicle") AS duplicate_group_size
    FROM staging.staged_delay_records d
    JOIN curated_selection s USING(snapshot_id)
), states AS MATERIALIZED (
    SELECT *, calendar_weekday(parsed_date) AS derived_weekday,
        CASE WHEN is_blank("Date") THEN 'missing' WHEN parsed_date IS NULL THEN 'invalid' ELSE 'valid' END AS date_status,
        CASE WHEN is_blank("Time") THEN 'missing' WHEN parsed_time IS NULL THEN 'invalid' ELSE 'valid' END AS time_status,
        CASE WHEN is_blank("Day") THEN 'missing' WHEN "Day" IN ('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday') THEN 'valid' ELSE 'unrecognized' END AS day_status,
        CASE WHEN is_blank("Min Delay") THEN 'missing' WHEN delay_minutes IS NULL THEN 'invalid' WHEN delay_minutes<0 THEN 'negative' ELSE 'valid' END AS delay_status,
        CASE WHEN is_blank("Min Gap") THEN 'missing' WHEN gap_value IS NULL THEN 'invalid' WHEN gap_value<0 THEN 'negative' ELSE 'valid' END AS gap_status,
        CASE WHEN parsed_date IS NULL THEN NULL WHEN is_blank("Day") THEN NULL ELSE "Day"<>calendar_weekday(parsed_date) END AS weekday_conflict,
        CASE WHEN parsed_date IS NOT NULL AND parsed_date>=:scope_start AND (:scope_end IS NULL OR parsed_date<=:scope_end) THEN 1 ELSE 0 END AS scope_eligible
    FROM parsed
)
SELECT snapshot_id,record_ordinal,source_mode,
    "_id","Date","Time","Day","Station","Code","Min Delay","Min Gap","Bound","Line","Vehicle",
    parsed_date,parsed_time,CAST(substr(parsed_time,1,2) AS INTEGER),derived_weekday,
    date_status,time_status,day_status,weekday_conflict,
    source_mode='bus' AND parsed_date IS NOT NULL AND substr("Date",11)<>'T00:00:00',
    delay_minutes,gap_value,delay_status,gap_status,'unresolved',
    delay_minutes>60,delay_minutes>120,delay_minutes>1440,
    CASE WHEN delay_minutes IS NOT NULL AND gap_value IS NOT NULL THEN gap_value<delay_minutes END,
    duplicate_group_size,duplicate_group_size>1,
    is_blank("Station"),is_blank("Line"),is_blank("Bound"),
    NOT is_blank("Bound") AND "Bound" NOT IN ('N','S','E','W'),
    is_blank("Vehicle"),"Vehicle"='0',instr("Line",'/')>0,length("Station")=22,
    CASE WHEN is_blank("Code") THEN 'missing' ELSE 'not_evaluated' END,NULL,
    1,scope_eligible,
    delay_status='valid',scope_eligible AND delay_status='valid',
    time_status='valid',scope_eligible AND time_status='valid',
    NOT is_blank("Line"),scope_eligible AND NOT is_blank("Line"),
    NOT is_blank("Code"),scope_eligible AND NOT is_blank("Code"),
    0,0,parsed_date IS NOT NULL,
    parsed_date IS NOT NULL AND weekday_conflict IS NOT 1,0
FROM states ORDER BY snapshot_id,record_ordinal;
