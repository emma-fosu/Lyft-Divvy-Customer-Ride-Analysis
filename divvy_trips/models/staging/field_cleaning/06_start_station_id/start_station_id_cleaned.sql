SELECT
    rn,
    TRIM(start_station_id) AS start_station_id
FROM
    {{ ref('stag_divvy_tripdata_2024') }}