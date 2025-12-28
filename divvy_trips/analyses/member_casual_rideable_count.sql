SELECT
    member_casual,
    rideable_type,
    COUNT(*) AS rideable_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(PARTITION BY member_casual), 1) AS count_perc
FROM
    {{ ref('cleaned_divvy_tripdata_2024') }}
GROUP BY member_casual, rideable_type
ORDER BY member_casual, rideable_type