SELECT
    rn,
    TRIM(end_station_name) AS end_station_name
FROM
    {{ ref('stag_divvy_tripdata_2024') }}
