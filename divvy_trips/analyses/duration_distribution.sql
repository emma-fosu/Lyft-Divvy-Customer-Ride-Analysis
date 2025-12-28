SELECT
    duration_cat,
    COUNT(*) AS dist
FROM (
    SELECT
        CASE
            WHEN TIMESTAMPDIFF(MINUTE, started_at, ended_at) <= 2 THEN "<2 MIN"
            WHEN TIMESTAMPDIFF(MINUTE, started_at, ended_at) <= 10 THEN "<10 MIN"
            WHEN TIMESTAMPDIFF(MINUTE, started_at, ended_at) <= 20 THEN "<20 MIN"
            WHEN TIMESTAMPDIFF(MINUTE, started_at, ended_at) <= 40 THEN "<40 MIN"
            WHEN TIMESTAMPDIFF(MINUTE, started_at, ended_at) <= 60 THEN "<60 MIN"
            WHEN TIMESTAMPDIFF(MINUTE, started_at, ended_at) <= 80 THEN "<80 MIN"
            WHEN TIMESTAMPDIFF(MINUTE, started_at, ended_at) <= 100 THEN "<100 MIN"
            ELSE "MORE"
        END AS duration_cat
    FROM
        {{ ref('cleaned_divvy_tripdata_2024') }}
)
GROUP BY duration_cat
ORDER BY duration_cat