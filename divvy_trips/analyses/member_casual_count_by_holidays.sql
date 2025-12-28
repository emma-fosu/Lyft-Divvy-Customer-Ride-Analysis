SELECT
    member_casual,
    holiday_name,
    COUNT(*) AS total_sub_rides,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(PARTITION BY u.holiday_name), 1) AS count_perc
FROM
    {{ ref('cleaned_divvy_tripdata_2024') }} c
INNER JOIN {{ ref('us_holidays_2024') }} u
ON TO_DATE(c.started_at) = u.date
GROUP BY u.holiday_name, c.member_casual
ORDER BY u.holiday_name, member_casual