SELECT
    member_casual,
    COUNT(*) AS sub_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS count_perc
FROM
    {{ ref('cleaned_divvy_tripdata_2024') }}
WHERE TIMESTAMPDIFF(MINUTE, started_at, ended_at) >= 30
GROUP BY member_casual