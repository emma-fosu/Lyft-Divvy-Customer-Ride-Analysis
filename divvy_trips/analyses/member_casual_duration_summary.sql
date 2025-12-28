SELECT
    member_casual,
    MIN(TIMESTAMPDIFF(MINUTE, started_at, ended_at)) AS min_duration,
    MAX(TIMESTAMPDIFF(MINUTE, started_at, ended_at)) AS max_duration,
    MAX(TIMESTAMPDIFF(MINUTE, started_at, ended_at)) - MIN(TIMESTAMPDIFF(MINUTE, started_at, ended_at)) AS range,
    AVG(TIMESTAMPDIFF(MINUTE, started_at, ended_at)) AS mean_duration,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY TIMESTAMPDIFF(MINUTE, started_at, ended_at)) AS median_duration,
    STDDEV(TIMESTAMPDIFF(MINUTE, started_at, ended_at)) AS stddev_duration
FROM
    {{ ref('cleaned_divvy_tripdata_2024') }}
GROUP BY member_casual