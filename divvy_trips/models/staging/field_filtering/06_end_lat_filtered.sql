SELECT
    *
FROM
    {{ ref('05_start_lng_filtered') }}
WHERE
    end_lat >= 41.6 AND end_lat <= 42.1