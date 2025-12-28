SELECT
    member_casual AS `Rider Type`,
    COUNT(*) AS `Total Rides`,
    ROUND(COUNT(*) / SUM(COUNT(*)) OVER (), 4) AS `Proportion (%)`
FROM
    {{ ref('cleaned_divvy_tripdata_2024') }}
GROUP BY
    member_casual