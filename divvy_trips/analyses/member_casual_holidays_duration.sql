SELECT
    member_casual,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY TIMESTAMPDIFF(MINUTE, started_at, ended_at)) AS med_duration,
    AVG(TIMESTAMPDIFF(MINUTE, started_at, ended_at)) AS avg_duration
FROM
    {{ ref('cleaned_divvy_tripdata_2024') }} c
INNER JOIN {{ ref('us_holidays_2024') }} u
GROUP BY member_casual