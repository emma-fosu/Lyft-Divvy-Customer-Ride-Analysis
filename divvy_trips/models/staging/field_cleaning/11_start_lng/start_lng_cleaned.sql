SELECT
    rn,
    ROUND(start_lng, 5) AS start_lng
FROM
    {{ ref('stag_divvy_tripdata_2024') }}