SELECT
    *
FROM
    {{ ref('01_ride_id_filtered') }}
WHERE started_at < ended_at