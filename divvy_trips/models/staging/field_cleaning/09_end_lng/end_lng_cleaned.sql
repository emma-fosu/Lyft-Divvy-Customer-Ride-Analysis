SELECT
    rn,
    ROUND(end_lng, 5) AS end_lng
FROM
    {{ ref('stag_divvy_tripdata_2024') }}