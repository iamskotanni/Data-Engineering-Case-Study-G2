
-- 1. CLEAR EXISTING TABLES (Ensures a fresh run since we rerun the script multiple times during development)

DROP TABLE IF EXISTS fact_reviews;
DROP TABLE IF EXISTS fact_weather;
DROP TABLE IF EXISTS dim_date;
DROP TABLE IF EXISTS dim_listing;

-- 2. CREATE DIMENSION TABLES 

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

-- 3. CREATE FACT TABLES 

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
   sentiment_stars DOUBLE,
   weather_category VARCHAR,
   weather_sentence VARCHAR,
   weather_sentiment_score DOUBLE
);

-- 4. POPULATE DIMENSION TABLES

INSERT INTO dim_listing
SELECT DISTINCT
   CAST(listing_id AS BIGINT),
   CAST(neighbourhood_cleansed AS VARCHAR),
   CAST(property_type AS VARCHAR),
   CAST(room_type AS VARCHAR),
   CAST(host_is_superhost AS BOOLEAN),
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

-- 5. POPULATE FACT TABLES

INSERT INTO fact_weather
SELECT DISTINCT
   CAST(date AS DATE) AS date_key,
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
   CAST(date AS DATE) AS date_key,
   CAST(sentiment_stars AS DOUBLE),
   CAST(weather_category AS VARCHAR),
   CAST(weather_sentence AS VARCHAR),
   CAST(weather_sentiment_score AS DOUBLE)
FROM staging_table
WHERE id_x IS NOT NULL;