SELECT
    *
FROM
    {{ ref('03_duration_filtered') }}
WHERE NOT (end_station_name IS NULL AND (end_lat IS NULL AND end_lng IS NULL))