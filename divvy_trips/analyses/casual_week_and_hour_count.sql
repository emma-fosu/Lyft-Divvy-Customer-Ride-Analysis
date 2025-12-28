SELECT
    member_casual AS `Rider Type`,
    day_of_week AS `Day of Week`,
    hour_am_pm AS `Hour of Day`,
    COUNT(*) AS `Rides Count`,
    PERCENTILE_CONT(0.5) WITHIN GROUP(ORDER BY TIMESTAMPDIFF(MINUTE, started_at, ended_at)) AS `Duration (min)`,
    day_of_week_num AS `Day of Week Sort`,
    hour_num AS `Hour of Day Sort`
FROM
    {{ ref('cleaned_divvy_tripdata_2024') }} c
LEFT JOIN {{ ref('divvy_tripdata_date') }} d
ON c.started_at = d.ride_datetime
GROUP BY member_casual, day_of_week, day_of_week_num, hour_am_pm, hour_num
ORDER BY day_of_week_num, hour_num