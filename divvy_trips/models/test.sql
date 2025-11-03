SELECT
    *
FROM
    {{ source('divvy_trip_app', '202404_divvy_tripdata') }}
LIMIT 5;