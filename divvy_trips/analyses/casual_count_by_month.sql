SELECT
    month AS  Month,
    month_num AS `Month Sort`,
    COUNT(*) AS `Ride Count`,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY TIMESTAMPDIFF(MINUTE, started_at, ended_at)) AS `Duration (min)`
FROM
    {{ ref('cleaned_divvy_tripdata_2024') }} c
LEFT JOIN {{ ref('divvy_tripdata_date') }} d
ON c.started_at = d.ride_datetime
WHERE member_casual = "Casual"
GROUP BY member_casual, month, d.month_num
ORDER BY d.month_num, member_casual