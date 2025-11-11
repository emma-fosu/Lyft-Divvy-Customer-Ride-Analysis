SELECT
    rn,
    COALESCE(TRIM(start_station_id), "Unknown ID") AS start_station_id
FROM
    {{ ref('stag_divvy_tripdata_2024') }}