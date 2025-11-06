SELECT *
FROM {{ ref('ride_id_cleaned') }}
INNER JOIN {{ ref('rideable_type_cleaned') }} USING (rn)
INNER JOIN {{ ref('member_casual_cleaned') }} USING (rn)
INNER JOIN {{ ref('start_station_name_cleaned') }} USING (rn)
INNER JOIN {{ ref('end_station_name_cleaned') }} USING (rn)
INNER JOIN {{ ref('end_station_id_cleaned') }} USING (rn)
INNER JOIN {{ ref('start_station_id_cleaned') }} USING (rn)
INNER JOIN {{ ref('end_lat_cleaned') }} USING (rn)
INNER JOIN {{ ref('end_lng_cleaned') }} USING (rn)
INNER JOIN {{ ref('start_lat_cleaned') }} USING (rn)
INNER JOIN {{ ref('start_lng_cleaned') }} USING (rn)
INNER JOIN {{ ref('started_at_cleaned') }} USING (rn)
INNER JOIN {{ ref('ended_at_cleaned') }} USING (rn)
ORDER BY rn