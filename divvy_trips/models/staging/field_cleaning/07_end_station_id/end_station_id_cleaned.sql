SELECT
    rn,
    COALESCE(TRIM(end_station_id), "Unknown ID") AS end_station_id
FROM
    {{ ref('stag_divvy_tripdata_2024') }}