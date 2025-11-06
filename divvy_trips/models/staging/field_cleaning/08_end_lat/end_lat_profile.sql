WITH lat_outside_chicago_duration_distribution (
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
    WHERE NOT (end_lat BETWEEN 41.6 AND 42.1)
    GROUP BY duration_bucket
    ORDER BY MIN(TIMESTAMPDIFF(MINUTE, started_at, ended_at))
)

SELECT *
FROM lat_outside_chicago_duration_distribution

{# Ride ending outside Chicago duration seems normal #}