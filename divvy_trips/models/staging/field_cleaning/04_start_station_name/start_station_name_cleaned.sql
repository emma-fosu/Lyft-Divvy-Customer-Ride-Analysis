SELECT
    rn,
    COALESCE(TRIM(BOTH '*' FROM TRIM(start_station_name)), "Unknown Station") AS start_station_name
FROM
    {{ ref('stag_divvy_tripdata_2024') }}