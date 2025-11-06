{{
  config(
    materialized = 'table',
    )
}}

{%- set months = range(1, 13) -%}
{%- set table_names = [] -%}
{%- for month in months -%}
  {%- do table_names.append("2024" ~ "{:02d}".format(month) ~ "_divvy_tripdata") -%}
{% endfor %}

{%- for table_name in table_names -%}
    SELECT *
    FROM {{ source('divvy_trip_app', table_name) }}
    {% if not loop.last %}
      UNION ALL
    {% endif %}
{% endfor %}