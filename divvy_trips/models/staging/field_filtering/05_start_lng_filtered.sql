SELECT
    *
FROM
    {{ ref('04_end_station_name_filtered') }}
WHERE 
    start_lng >= -87.9 AND start_lng <= -87.5