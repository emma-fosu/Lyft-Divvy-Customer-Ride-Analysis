SELECT
    rn,
    TRIM(start_station_name) AS start_station_name
FROM
    {{ ref('stag_divvy_tripdata_2024') }}