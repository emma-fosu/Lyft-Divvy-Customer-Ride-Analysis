SELECT
    member_casual,
    day_of_week,
    ROUND(AVG(TIMESTAMPDIFF(MINUTE, started_at, ended_at))) AS avg_duration_min,
    PERCENTILE_CONT(0.5) WITHIN GROUP(ORDER BY TIMESTAMPDIFF(MINUTE, started_at, ended_at)) AS med_duration_min
FROM
    {{ ref('cleaned_divvy_tripdata_2024') }} c
LEFT JOIN {{ ref('divvy_tripdata_date') }} d
ON c.started_at = d.ride_datetime
GROUP BY member_casual, day_of_week, d.day_of_week_num
ORDER BY d.day_of_week_num, member_casual