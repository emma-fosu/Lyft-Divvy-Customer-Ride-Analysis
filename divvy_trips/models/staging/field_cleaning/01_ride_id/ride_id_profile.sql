WITH duplicate_rides AS (
    SELECT
        ride_id,
        COUNT(*) as d_count
    FROM
        {{ ref('stag_divvy_tripdata_2024') }}
    GROUP BY ride_id
    HAVING COUNT(ride_id) > 1
), 
duplicate_rides_info AS (
    SELECT
        ride_id,
        started_at,
        ended_at
    FROM
        duplicate_rides
    INNER JOIN
        {{ ref('stag_divvy_tripdata_2024') }}
    USING (ride_id)
), 
time_prev AS (
    SELECT
        ride_id,
        started_at,
        ended_at,
        LAG(started_at) OVER(PARTITION BY ride_id ORDER BY started_at) AS prev_started_at,
        LAG(ended_at) OVER(PARTITION BY ride_id ORDER BY ended_at) AS prev_ended_at
    FROM duplicate_rides_info  
), 
time_diff AS (
    SELECT
        ride_id,
        AVG(UNIX_TIMESTAMP(prev_started_at) - UNIX_TIMESTAMP(started_at)) AS started_diff_time,
        AVG(UNIX_TIMESTAMP(prev_ended_at) - UNIX_TIMESTAMP(ended_at)) AS ended_diff_time
    FROM
        time_prev
    WHERE prev_started_at IS NOT NULL OR prev_ended_at IS NOT NULL
    GROUP BY ride_id
)

SELECT * FROM time_diff

{# The duplicate rides record seem to be the same because their start time and end time difference is 0 #}
{# Action: Remove one of the duplicated ride #}