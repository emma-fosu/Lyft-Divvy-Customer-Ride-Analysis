SELECT
    member_casual AS `Rider Type`,
    end_station_name AS `Station Name`,
    lng,
    lat,
    ride_count AS `Ride Count`
FROM (
        SELECT
        member_casual,
        end_station_name,
        MIN(end_lng) AS lng,
        MIN(end_lat) AS lat,
        COUNT(*) AS ride_count,
        ROW_NUMBER() OVER(PARTITION BY member_casual ORDER BY COUNT(*) DESC) AS rn
    FROM
        {{ ref('cleaned_divvy_tripdata_2024') }}
    WHERE end_station_name <> 'Unknown Station'
    GROUP BY member_casual, end_station_name
) AS r
WHERE rn BETWEEN 1 AND 10