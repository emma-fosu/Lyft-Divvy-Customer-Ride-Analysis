SELECT
    *
FROM
    {{ ref('06_end_lat_filtered') }}
WHERE end_lng >= -87.9 AND end_lng <= -87.5