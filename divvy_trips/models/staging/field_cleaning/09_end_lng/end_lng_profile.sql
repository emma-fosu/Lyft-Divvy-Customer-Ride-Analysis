WITH lng_outside_chicago_duration_distribution AS(
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
    WHERE NOT (end_lng BETWEEN -87.9 AND -87.51)
    GROUP BY duration_bucket, sort_key
)

SELECT duration_bucket, num_rides
FROM lng_outside_chicago_duration_distribution
ORDER BY sort_key


{# Ride ending outside Chicago duration seems normal #}