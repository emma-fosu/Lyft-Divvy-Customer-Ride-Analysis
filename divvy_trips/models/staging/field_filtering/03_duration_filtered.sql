SELECT
    *
FROM
    {{ ref('02_started_at_filtered') }}
WHERE TIMESTAMPDIFF(Minute, started_at, ended_at) BETWEEN 1 AND 120