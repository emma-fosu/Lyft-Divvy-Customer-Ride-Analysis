SELECT
    member_casual,
    rideable_type,
    COUNT(*) AS rideable_count,
    COUNT(*) FILTER (WHERE TIMESTAMPDIFF(MINUTE, started_at, ended_at) <= 2) AS rideable_count_less_than_2min,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(PARTITION BY member_casual), 1) AS count_perc,
    ROUND((COUNT(*) FILTER (WHERE TIMESTAMPDIFF(MINUTE, started_at, ended_at) <= 2) * 100.0) / COUNT(*), 1) AS count_perc_less_than_2min
FROM
    {{ ref('cleaned_divvy_tripdata_2024') }}
GROUP BY member_casual, rideable_type
ORDER BY member_casual, rideable_type