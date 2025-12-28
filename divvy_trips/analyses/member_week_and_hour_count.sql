SELECT
    member_casual AS type,
    day_of_week AS day,
    hour_am_pm AS time,
    COUNT(*) AS ride_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(PARTITION BY day_of_week), 2) AS count_perc
FROM
    {{ ref('cleaned_divvy_tripdata_2024') }} c
LEFT JOIN {{ ref('divvy_tripdata_date') }} d
ON c.started_at = d.ride_datetime
WHERE member_casual = 'Member'
GROUP BY member_casual, day_of_week, day_of_week_num, hour_am_pm, hour_num
ORDER BY day_of_week_num, hour_num