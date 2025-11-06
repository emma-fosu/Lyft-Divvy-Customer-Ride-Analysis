SELECT
    rn,
    TRIM(end_station_id) AS end_station_id
FROM
    {{ ref('stag_divvy_tripdata_2024') }}