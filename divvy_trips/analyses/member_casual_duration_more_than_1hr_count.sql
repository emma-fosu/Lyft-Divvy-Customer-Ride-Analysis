SELECT
    member_casual,
    COUNT(*) AS sub_count
FROM
    {{ ref('cleaned_divvy_tripdata_2024') }}
WHERE TIMESTAMPDIFF(MINUTE, started_at, ended_at) >= 60
GROUP BY member_casual