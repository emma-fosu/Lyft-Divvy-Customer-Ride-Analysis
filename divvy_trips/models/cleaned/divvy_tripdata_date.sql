SELECT
    DISTINCT ride_datetime,
    TO_DATE(ride_datetime) AS ride_date,
    EXTRACT(YEAR FROM ride_datetime) AS year,
    EXTRACT(MONTH FROM ride_datetime) AS month_num,
    DATE_FORMAT(ride_datetime, 'MMMM') AS month,
    EXTRACT(WEEK FROM ride_datetime) AS week_of_year,
    (DAYOFWEEK(ride_datetime) + 5) % 7 + 1 AS day_of_week_num,
    DATE_FORMAT(ride_datetime, 'EEEE') AS day_of_week,
    DATE_FORMAT(ride_datetime, 'h a') AS hour_am_pm
FROM (
    SELECT
        DISTINCT started_at AS ride_datetime
    FROM
        {{ ref('cleaned_divvy_tripdata_2024') }}
    UNION ALL
    SELECT
        DISTINCT ended_at AS ride_datetime
    FROM
        {{ ref('cleaned_divvy_tripdata_2024') }}
)
ORDER BY ride_datetime