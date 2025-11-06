SELECT
    ROW_NUMBER() OVER(ORDER BY ride_id) as rn,
    *
FROM
    {{ ref('divvy_tripdata_2024') }}