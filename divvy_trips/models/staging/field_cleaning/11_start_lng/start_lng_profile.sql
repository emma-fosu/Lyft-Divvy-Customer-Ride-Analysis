WITH lng_outside_chicago_duration_distribution (
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
    WHERE NOT (start_lng BETWEEN -87.9 AND -87.51)
    GROUP BY duration_bucket
    ORDER BY MIN(TIMESTAMPDIFF(MINUTE, started_at, ended_at))
)

SELECT *
FROM lng_outside_chicago_duration_distribution


{# Only one ride started outside Chicago and that ride is normal #}