SELECT
    rn,
    ROUND(start_lat, 5) AS start_lat
FROM
    {{ ref('stag_divvy_tripdata_2024') }}