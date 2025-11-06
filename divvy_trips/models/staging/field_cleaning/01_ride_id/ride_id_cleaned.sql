SELECT
    rn,
    TRIM(ride_id) AS ride_id
FROM
    {{ ref('stag_divvy_tripdata_2024') }}