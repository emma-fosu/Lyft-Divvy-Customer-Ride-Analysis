SELECT
    rn,
    CASE
        WHEN TRIM(rideable_type) = "electric_bike" THEN "Electric Bike"
        WHEN TRIM(rideable_type) = "classic_bike" THEN "Classic Bike"
        WHEN TRIM(rideable_type) = "scooter" THEN "scooter"
        WHEN TRIM(rideable_type) = "electric_scooter" THEN "Electric Scooter"
        ELSE "Unknown Rideable"
    END AS rideable_type
FROM
    {{ ref('stag_divvy_tripdata_2024') }}