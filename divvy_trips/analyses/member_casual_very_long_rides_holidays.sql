WITH very_long_rides AS (
    SELECT
        ride_id,
        started_at
    FROM
        {{ ref('cleaned_divvy_tripdata_2024') }}
    WHERE TIMESTAMPDIFF(MINUTE, started_at, ended_at) >= 60
), very_long_rides_count AS (
    SELECT
        COUNT(*) AS ride_count
    FROM
        very_long_rides
), very_long_ride_holidays_count AS (
    SELECT
        COUNT(*) AS ride_holiday_count
    FROM
        very_long_rides v
    INNER JOIN {{ ref('us_holidays_2024') }} u
    ON TO_DATE(v.started_at) = u.date 
), member_

SELECT
    ride_count,
    ride_holiday_count,
    ROUND(ride_holiday_count * 100.0 / ride_count, 2) AS count_perc
FROM
    very_long_rides_count
CROSS JOIN very_long_ride_holidays_count