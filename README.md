### Dataset
This data is provided according to the Divvy Data License Agreement and released on a monthly schedule. 

The data has been processed to remove trips that are taken by staff as they service and inspect the system; and any trips that were below **60** seconds in length (potentially false starts or users trying to re-dock a bike to ensure it was secure).
You can read more about the dataset [here](https://divvybikes.com/system-data).

This project only considered trips for **2024**.

Each trip is **anonymized** and includes the following fields:

| field | type | description|
|-------|------|------------|
| ride_id | string | Unique ride identifier |
| rideable_type | string | Types of rideable |
| started_at | timestamp | Ride start time |
| ended_at | timestamp | Ride end time |
| start_station_name | string | Ride start station name |
| end_station_name | string | Ride end station name |
| start_station_id | string | Ride start station id |
| end_station_id | string | Ride end station id |
| start_lat | double | Ride starting latitude |
| start_lng | double | Ride starting longitude |
| end_lat | double | Ride ending latitude |
| end_lng | double | Ride ending longtitude|
| member_casual | string | Subscriber type |

### Data Sourcing and Platform
The Divvy trip dataset for 2024 was provided as 12 separate CSV files, each named according to the format `YYYYMM_divvy_tripdata.csv`. These monthly files were uploaded to the **Databricks** platform, where data transformations and modeling were managed using **dbt (Data Build Tool)**. Using **dbt**, all 12 monthly datasets were combined into a single consolidated CSV file (`divvy_tripdata_2024.csv`).
```sql
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
```
*This is the dbt sql to create an table appending all 12 datasets.*

#### Data testing
The new table (`divvy_tripdata_2024`) containing the appended datasets was tested with **dbt generic test macros**.
*The table show which field was tested and what test was made.*
| **Column** | **Type** | **Test Type** | **Description / Purpose**|
| -----------| ---------|---------------|--------------------------|
| `ride_id` | string | `not_null` | Ensure every record has a unique ride identifier |
|           |        | `unique` | Guarantee each `ride_id` is unique (no duplicates) |
| `rideable_type` | string | `not_null` | Ensure no missing bike type |
|                 |        | `accepted_values` | Only valid bike types allowed (electric_bike, classic_bike, scooter) | 
| `started_at` | timestamp | `not_null` | Each trip must have a start time |
|              |           | `expression_is_true` | Start time must be before end time | 
| `ended_at` | timestamp | `not_null` | Each trip must have an end time |
|            |           | `expression_is_true`| Trip duration must be within valid range (e.g., 0–24 hrs) |
| `start_station_name` | string | `not_null` *(optional)* | Ensure name is present for most records |
|                      |        | `expression_is_true` | Name must exist if ID exists | 
| `start_station_id` | string | `expression_is_true` | Station ID should follow a valid format |
|                    |         | `expression_is_true` | Should not be null when name exists | 
| `end_station_name` | string    | `not_null` *(optional)* | Ensure destination name is filled | 
|                      |           | `expression_is_true` | Should have station ID if name exists |
| `end_station_id` | string | `expression_is_true` | Station ID should follow valid format |
| `start_lat` | double | `expression_is_true` | Latitude must fall within Chicago area (~41.6–42.1° N) | 
| `start_lng` | double | `expression_is_true` | Longitude must fall within Chicago area (~-87.9–-87.5° W) |
| `end_lat` | double | `expression_is_true` | End latitude must fall within Chicago area |
| `end_lng` | double | `expression_is_true` | End longitude must fall within Chicago area |
| `member_casual` | string  | `not_null` | Membership type must be present  |
|                 |         | `accepted_values` | Only “member” or “casual” allowed |


| Column Tested | Description | Failed Records Count | Meaning / Likely Issue | Suggested Action |
|----------------|--------------|----------------|------------------------|------------------|
| `end_lat` | Checks if `end_lat` is within valid Chicago bounds (41.6 – 42.1). | **84** | 84 trips have ending latitude outside the valid geographic range. | Inspect and remove or correct invalid coordinates (possible GPS errors). |
| `end_lng` | Checks if `end_lng` is within valid longitude range (-87.9 – -87.5). | **106** | 106 trips have longitude values outside expected bounds. | Validate and filter out invalid `end_lng` points. |
| `ended_at` | Ensures `ended_at` > `started_at`. | **227** | 227 rides have end times earlier than start times — invalid durations. | Drop or investigate rows with negative durations. |
| `start_lng` | Checks if `start_lng` is within valid longitude range (-87.9 – -87.5). | **1** | 1 ride’s start longitude is out of bounds. | Review and filter this record. |
| `started_at` | Ensures `started_at` < `ended_at`. | **227** | Same 227 rides likely flagged again. | Remove duplicates of this test; keep one direction check. |
| `ride_id` | Ensures `ride_id` values are unique. | **211** | 211 rides share duplicate `ride_id` values. | Deduplicate records before further processing. |



### Data Cleaning and Transformation




| **Column** | **Type** | **Test Type** | **Description / Purpose**|
| -----------| ---------|---------------|--------------------------|
| `ride_id` | string | `not_null` | Ensure every record has a unique ride identifier |
|           |        | `unique` | Guarantee each `ride_id` is unique (no duplicates) |
| `rideable_type` | string | `not_null` | Ensure no missing bike type |
|                 |        | `accepted_values` | Only valid bike types allowed | 
| `started_at` | timestamp | `not_null` | Each trip must have a start time |
|              |           | `expression_is_true` | Start time must be before end time | 
| `ended_at` | timestamp | `not_null` | Each trip must have an end time |
|            |           | `expression_is_true`| Trip duration must be within valid range (e.g., 0–24 hrs) |
| `start_station_name` | string | `not_null` *(optional)* | Ensure name is present for most records |
|                      |        | `expression_is_true` | Name must exist if ID exists | 
| `start_station_id` | string | `expression_is_true` | Station ID should follow a valid format |
|                    |         | `expression_is_true` | Should not be null when name exists | 
| `end_station_name` | string    | `not_null` *(optional)* | Ensure destination name is filled | 
|                      |           | `expression_is_true` | Should have station ID if name exists |
| `end_station_id` | string | `expression_is_true` | Station ID should follow valid format |
| `start_lat` | double | `expression_is_true` | Latitude must fall within Chicago area (~41.6–42.1° N) | 
| `start_lng` | double | `expression_is_true` | Longitude must fall within Chicago area (~-87.9–-87.5° W) |
| `end_lat` | double | `expression_is_true` | End latitude must fall within Chicago area |
| `end_lng` | double | `expression_is_true` | End longitude must fall within Chicago area |
| `member_casual` | string  | `not_null` | Membership type must be present  |
|                 |         | `accepted_values` | Only “member” or “casual” allowed |

### Additional Data Tables
1. **Ride Date Table**: This table provides time-based attributes derived from each ride’s timestamp (ride_datetime). It is designed to support detailed temporal analysis of ride behavior, trends, and patterns such as demand by day, month, hour, or weekday.

| **Column Name** | **Data Type** |**Description** |
| ----------------| ------------- | ---------------|
| **ride_datetime** | `timestamp` | The exact date and time when the ride event occurred. This is the raw timestamp from which other time attributes are derived. |
| **ride_date** | `date` | The calendar date (without time) extracted from `ride_datetime`. Useful for grouping or filtering rides by date. |
| **year** | `int` | The four-digit year in which the ride took place (e.g., 2024). |
| **month_num** | `int` | The numeric value of the month (1–12) corresponding to `ride_datetime`. |
| **month** | `string` | The full or abbreviated month name (e.g., “January”). |
| **week_of_year** | `int` | The week number of the year (1–52) when the ride occurred.  |
| **day_of_week_num** | `int` | Numeric representation of the day of the week (e.g., 1 = Monday, 7 = Sunday). |
| **day_of_week** | `string` | Textual representation of the day of the week (e.g., “Monday”, “Tuesday”). |
| **hour_am_pm** | `string` | The hour of the ride with AM/PM designation (e.g., “08 AM”, “03 PM”). |

### Purpose and Use
1. This table serves as a time dimension for ride data analysis. It allows data analysts and engineers to:
2. Aggregate rides by date, day, or hour for trend analysis.
3. Identify peak riding hours and weekday vs weekend demand.
4. Perform seasonal, monthly, and yearly comparisons.
5. Simplify joins with ride fact tables in analytics pipelines.

2. **US Holidays Table**:
This table contains a list of recognized holidays with their corresponding dates. It serves as a reference for identifying whether a given ride or event occurred on a holiday, supporting temporal and behavioral analyses such as demand variation, staffing, or scheduling around public holidays.

| **Column Name**  | **Data Type** | **Description** |
| ---------------- | ------------- | --------------- |
| **date** | `date` | The calendar date of the holiday (in `yyyy-MM-dd` format). This field is used to join with the `ride_date` column in other tables for identifying rides occurring on holidays. |
| **holiday_name** | `string` | The official name or title of the holiday (e.g., “New Year’s Day”, “Independence Day”). |

