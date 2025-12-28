SELECT
    member_casual,
    hour_am_pm,
    COUNT(*) AS total_sub_rides,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(PARTITION BY hour_am_pm), 2) AS count_perc
FROM
    {{ ref('cleaned_divvy_tripdata_2024') }} c
LEFT JOIN {{ ref('divvy_tripdata_date') }} d
ON c.started_at = d.ride_datetime
GROUP BY member_casual, d.hour_num, d.hour_am_pm 
ORDER BY d.hour_num, member_casual