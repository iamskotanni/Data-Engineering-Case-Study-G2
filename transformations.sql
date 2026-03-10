/* ========================================================================
  
  Phase: Data Transformation (DDL & DML)
  Description: This script transforms the flat CLEANED_DATA_V2.csv
               into a Kimball Dimensional Model (Star Schema).
======================================================================== */

-- PART 1: DDL (Data Definition Language) - Building the Racks

CREATE TABLE dim_listing (
   listing_id BIGINT PRIMARY KEY,
   neighbourhood_cleansed VARCHAR,
   property_type VARCHAR,
   room_type VARCHAR,
   host_is_superhost BOOLEAN,
   price DOUBLE
);
CREATE TABLE dim_date (
   date_key DATE PRIMARY KEY,
   day_of_week VARCHAR,
   is_weekend BOOLEAN
);
CREATE TABLE fact_weather (
   date_key DATE PRIMARY KEY,
   temp_max DOUBLE,
   temp_min DOUBLE,
   apparent_temp_max DOUBLE,
   apparent_temp_min DOUBLE,
   rain DOUBLE,
   wind_speed DOUBLE,
   wind_gust DOUBLE,
   humidity DOUBLE
);
CREATE TABLE fact_reviews (
   review_id BIGINT PRIMARY KEY,
   listing_id BIGINT,
   date_key DATE,
   sentiment_stars DOUBLE
);

-- PART 2: DML (Data Manipulation Language) - Loading the Data
-- DuckDB reads the 'staging_table' directly from our Python environment

INSERT INTO dim_listing
SELECT DISTINCT
   CAST(listing_id AS BIGINT),
   neighbourhood_cleansed,
   property_type,
   room_type,
   CASE WHEN host_is_superhost = 't' THEN TRUE ELSE FALSE END,
   CAST(price AS DOUBLE)
FROM staging_table
WHERE listing_id IS NOT NULL;
INSERT INTO dim_date
SELECT DISTINCT
   CAST(date AS DATE) AS date_key,
   DAYNAME(CAST(date AS DATE)) AS day_of_week,
   CASE WHEN DAYOFWEEK(CAST(date AS DATE)) IN (0, 6) THEN TRUE ELSE FALSE END AS is_weekend
FROM staging_table
WHERE date IS NOT NULL;
INSERT INTO fact_weather
SELECT DISTINCT
   CAST(date AS DATE),
   CAST(temp_max AS DOUBLE),
   CAST(temp_min AS DOUBLE),
   CAST(apparent_temp_max AS DOUBLE),
   CAST(apparent_temp_min AS DOUBLE),
   CAST(rain AS DOUBLE),
   CAST(wind_speed AS DOUBLE),
   CAST(wind_gust AS DOUBLE),
   CAST(humidity AS DOUBLE)
FROM staging_table
WHERE date IS NOT NULL;
INSERT INTO fact_reviews
SELECT DISTINCT
   CAST(id_x AS BIGINT) AS review_id,
   CAST(listing_id AS BIGINT),
   CAST(date AS DATE),
   CAST(sentiment_stars AS DOUBLE)
FROM staging_table
WHERE id_x IS NOT NULL;