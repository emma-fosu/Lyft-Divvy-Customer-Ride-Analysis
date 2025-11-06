WITH station_with_no_name_count AS (
    SELECT
        COUNT(*) AS station_with_no_name_count
    FROM
        {{ ref('stag_divvy_tripdata_2024') }}
    WHERE start_station_name IS NULL
), station_with_no_name_and_id_count AS (
    SELECT
        COUNT(*) AS station_with_no_name_and_id_count
    FROM
        {{ ref('stag_divvy_tripdata_2024') }}
    WHERE start_station_name IS NULL AND start_station_id IS NULL
), station_with_no_name_start_lng_start_lat AS (
    SELECT
        COUNT(*) AS station_with_no_name_start_lng_start_lat
    FROM
        {{ ref('stag_divvy_tripdata_2024') }}
    WHERE start_station_name IS NULL AND start_lng IS NULL AND start_lat IS NULL
), station_with_no_name_duration_distribution AS (
    SELECT
        CASE
            WHEN TIMESTAMPDIFF(MINUTE, started_at, ended_at) < 1 THEN '<1 min'
            WHEN TIMESTAMPDIFF(MINUTE, started_at, ended_at) < 10 THEN '1-10 min'
            WHEN TIMESTAMPDIFF(MINUTE, started_at, ended_at) < 20 THEN '10-20 min'
            WHEN TIMESTAMPDIFF(MINUTE, started_at, ended_at) < 30 THEN '20-30 min'
            WHEN TIMESTAMPDIFF(MINUTE, started_at, ended_at) < 60 THEN '30-60 min'
            WHEN TIMESTAMPDIFF(MINUTE, started_at, ended_at) < 120 THEN '1-2 hrs'
            ELSE '2+ hrs'
        END AS duration_bucket,
        COUNT(*) AS num_rides
    FROM {{ ref('stag_divvy_tripdata_2024') }}
    WHERE start_station_name IS NULL AND ended_at > started_at
    GROUP BY duration_bucket
    ORDER BY MIN(TIMESTAMPDIFF(MINUTE, started_at, ended_at))
)

SELECT
    *
FROM
    {{ ref('station_information') }}

{# SELECT *  #}
{# FROM station_with_no_name_duration_distribution #}
{# All stations without a name also don't have an id #}
{# All stations without a name have both start lng and lat #}
{# The duration distribution for rides without station name is not abnormal #}

