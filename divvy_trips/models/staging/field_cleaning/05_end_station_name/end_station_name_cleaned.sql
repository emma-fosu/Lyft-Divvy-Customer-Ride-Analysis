SELECT
    rn,
    COALESCE(TRIM(BOTH '*' FROM TRIM(end_station_name)), "Unknown Station") AS end_station_name
FROM
    {{ ref('stag_divvy_tripdata_2024') }}
