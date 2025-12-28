
WITH member_casual_med_duration_distance AS (
    SELECT
        member_casual,
        TIMESTAMPDIFF(MINUTE, started_at, ended_at) AS duration_min,
        6371 * 2 * ASIN(
            SQRT(
                POWER(SIN(RADIANS(end_lat - start_lat) / 2), 2) +
                COS(RADIANS(start_lat)) * COS(RADIANS(end_lat)) *
                POWER(SIN(RADIANS(end_lng - start_lng) / 2), 2)
            )
        ) AS distance_km
    FROM
        {{ ref('cleaned_divvy_tripdata_2024') }}
)

SELECT
    member_casual AS `Rider Type`,
    PERCENTILE_CONT(0.5) WITHIN GROUP (
        ORDER BY duration_min
    ) AS `Duration (min)`,
    ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY distance_km), 2) AS `Distance (km)`
FROM
    member_casual_med_duration_distance
GROUP BY
    member_casual