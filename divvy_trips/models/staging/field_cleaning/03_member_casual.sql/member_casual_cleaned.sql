SELECT
    rn,
    INITCAP(TRIM(member_casual)) AS member_casual
FROM
    {{ ref('stag_divvy_tripdata_2024') }}