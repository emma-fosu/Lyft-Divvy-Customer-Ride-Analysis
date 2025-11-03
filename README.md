### Dataset
This data is provided according to the Divvy Data License Agreement and released on a monthly schedule. 

The data has been processed to remove trips that are taken by staff as they service and inspect the system; and any trips that were below **60 seconds in length (potentially false starts or users trying to re-dock a bike to ensure it was secure).
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