SELECT
    member_casual,
    day_of_week,
    COUNT(*) AS total_sub_rides,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(PARTITION BY day_of_week), 2) AS count_perc
FROM
    {{ ref('cleaned_divvy_tripdata_2024') }} c
LEFT JOIN {{ ref('divvy_tripdata_date') }} d
ON c.started_at = d.ride_datetime
GROUP BY member_casual, day_of_week, d.day_of_week_num
ORDER BY d.day_of_week_num, member_casual