{%- set fields = dbt_utils.get_filtered_columns_in_relation(from=ref("divvy_tripdata_2024"), except=["ride_id_rn", "rn"]) -%}
SELECT
    {% for field in fields %}
        {{ field }}
        {%- if not loop.last -%}
            ,
        {% endif %}
    {% endfor %}
FROM (
    SELECT
        *,
        ROW_NUMBER() OVER(PARTITION BY ride_id ORDER BY started_at) AS ride_id_rn
    FROM
        {{ ref('merge_cleaned_fields_divvy_tripdata_2024') }}
    ORDER BY ride_id
)
WHERE ride_id_rn = 1

