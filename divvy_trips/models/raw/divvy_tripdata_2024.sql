{{
  config(
    materialized = 'table',
    )
}}

{% set tables = dbt_utils.get_relations_by_pattern(
    schema_pattern='default',
    table_pattern='2024%_divvy_tripdata'
) %}

{% for table in tables %}
SELECT *
FROM {{ table }}
{% if not loop.last %}
UNION ALL
{% endif %}
{% endfor %}