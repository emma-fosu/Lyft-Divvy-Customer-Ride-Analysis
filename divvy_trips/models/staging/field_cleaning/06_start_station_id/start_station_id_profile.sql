WITH station_with_id_not_name_count AS (
    SELECT 
        COUNT(*) AS station_with_id_not_name_count
    FROM
        {{ ref('stag_divvy_tripdata_2024') }}
    WHERE
        start_station_name IS NULL AND start_station_id IS NOT NULL
),
station_with_name_not_id_count AS (
    SELECT 
        COUNT(*) AS station_with_id_not_name_count
    FROM
        {{ ref('stag_divvy_tripdata_2024') }}
    WHERE
        start_station_name IS NOT NULL AND start_station_id IS NULL
)

SELECT *
FROM station_with_id_not_name_count
CROSS JOIN station_with_name_not_id_count