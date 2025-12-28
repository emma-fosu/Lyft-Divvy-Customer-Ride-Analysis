
WITH station_with_no_name_count AS (
    SELECT
        COUNT(*) AS station_with_no_name_count
    FROM
        {{ ref('stag_divvy_tripdata_2024') }}
    WHERE end_station_name IS NULL
), station_with_no_name_and_id_count AS (
    SELECT
        COUNT(*) AS station_with_no_name_and_id_count
    FROM
        {{ ref('stag_divvy_tripdata_2024') }}
    WHERE end_station_name IS NULL AND end_station_id IS NULL
), station_with_no_name_end_lng_end_lat AS (
    SELECT
        COUNT(*) AS station_with_no_name_end_lng_end_lat
    FROM
        {{ ref('stag_divvy_tripdata_2024') }}
    WHERE end_station_name IS NULL AND end_lng IS NULL AND end_lat IS NULL
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
        COUNT(*) AS num_rides,
        CASE
            WHEN TIMESTAMPDIFF(MINUTE, started_at, ended_at) < 1 THEN 1
            WHEN TIMESTAMPDIFF(MINUTE, started_at, ended_at) < 10 THEN 2
            WHEN TIMESTAMPDIFF(MINUTE, started_at, ended_at) < 20 THEN 3
            WHEN TIMESTAMPDIFF(MINUTE, started_at, ended_at) < 30 THEN 4
            WHEN TIMESTAMPDIFF(MINUTE, started_at, ended_at) < 60 THEN 5
            WHEN TIMESTAMPDIFF(MINUTE, started_at, ended_at) < 120 THEN 6
            ELSE 7
        END AS sort_key
    FROM {{ ref('stag_divvy_tripdata_2024') }}
    WHERE end_station_name IS NULL AND ended_at > started_at
    GROUP BY duration_bucket, sort_key
), station_with_no_name_end_lat_lng_duration_distribution AS (
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
        COUNT(*) AS num_rides,
         CASE
            WHEN TIMESTAMPDIFF(MINUTE, started_at, ended_at) < 1 THEN 1
            WHEN TIMESTAMPDIFF(MINUTE, started_at, ended_at) < 10 THEN 2
            WHEN TIMESTAMPDIFF(MINUTE, started_at, ended_at) < 20 THEN 3
            WHEN TIMESTAMPDIFF(MINUTE, started_at, ended_at) < 30 THEN 4
            WHEN TIMESTAMPDIFF(MINUTE, started_at, ended_at) < 60 THEN 5
            WHEN TIMESTAMPDIFF(MINUTE, started_at, ended_at) < 120 THEN 6
            ELSE 7
        END AS sort_key
    FROM {{ ref('stag_divvy_tripdata_2024') }}
    WHERE end_station_name IS NULL AND end_lat IS NULL AND end_lng IS NULL AND ended_at > started_at
    GROUP BY duration_bucket, sort_key
)

SELECT
    *
FROM station_with_no_name_end_lat_lng_duration_distribution

{# SELECT *  #}
{# FROM station_with_no_name_duration_distribution #}
{# All stations without a name also don't have an id #}
{# Some stations without a name also have no end lat and lng #}
{# Stations without and and no coordinates have an abnormal duration distribution #}
{# Action: Filter rides with no end station name and coordinates #}
