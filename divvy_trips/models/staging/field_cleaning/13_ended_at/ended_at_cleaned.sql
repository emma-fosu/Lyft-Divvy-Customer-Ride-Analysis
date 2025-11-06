SELECT
    rn,
    ended_at
FROM
    {{ ref('stag_divvy_tripdata_2024') }}
