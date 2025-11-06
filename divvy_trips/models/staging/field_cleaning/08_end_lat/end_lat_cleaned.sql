SELECT
    rn,
    ROUND(end_lat, 5) AS end_lat
FROM
    {{ ref('stag_divvy_tripdata_2024') }}