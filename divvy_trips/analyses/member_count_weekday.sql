SELECT
    day_of_week AS `Day of Week`,
    COUNT(*) AS `Ride Count`,
    day_of_week_num AS `Day of Week Sort`,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY TIMESTAMPDIFF(MINUTE, started_at, ended_at)) AS `Duration (min)`
FROM
    {{ ref('cleaned_divvy_tripdata_2024') }} c
LEFT JOIN {{ ref('divvy_tripdata_date') }} d
ON c.started_at = d.ride_datetime
WHERE member_casual = "Member"
GROUP BY day_of_week, d.day_of_week_num
ORDER BY d.day_of_week_num