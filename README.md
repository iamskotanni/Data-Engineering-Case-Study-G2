Data Pipeline & Architecture Overview

Project Objective
The goal of this data engineering pipeline is to transform raw Airbnb listings, reviews, and Cape Town historical weather data into a clean, query-optimized Kimball Star Schema. This architecture allows us to analyze the correlation between environmental factors (rain, wind, heat) and guest satisfaction (review sentiment) in Power BI.

Pipeline Architecture
We designed a three-stage ETL (Extract, Transform, Load) pipeline using Python for Natural Language Processing (NLP) and DuckDB for SQL-based data modeling.

Phase 1: Data Cleaning & NLP Sentiment Engine

Script: process_data.py
Input: FULL DATA MERGED.csv (Raw combined dataset)
Output: CLEANED_DATA_V2.csv (Processed flat file)
In this phase, we handled initial data cleaning (e.g., formatting price columns) and applied advanced Machine Learning to quantify qualitative guest reviews:

1. Granular Sentiment Analysis: We utilized the Hugging Face nlptown/bert-base-multilingual-uncased-sentiment model. To avoid blunt integer ratings (1-5), we engineered a weighted-average probability function to calculate precise, continuous decimal scores (e.g., 4.27) for every review, allowing for highly accurate scatter plot distributions.

2. Aspect-Based Weather Flagging: We implemented a "Regex Mega-Dictionary" to scan reviews for explicit weather mentions (rain, wind, heat, cold). If a guest mentioned the weather, the script isolates that specific sentence and runs a secondary NLP sentiment pass exclusively on the weather comment.

3. Data Reduction: Dropped heavy text columns after extracting the mathematical scores to optimize processing speed and file size.


Phase 2: Relational Data Modeling

Scripts: run_sql.py (Execution Engine) & transformations.sql (DDL/DML Logic)
Input: CLEANED_DATA_V2.csv
Output: 4x Star Schema CSVs (dim_listing.csv, dim_date.csv, fact_weather.csv, fact_reviews.csv)

Instead of feeding a flat file into Power BI, we used DuckDB as an in-memory SQL engine to enforce strict data governance and build a multi-fact Star Schema (Fact Constellation):
• Data Integrity: Applied IS NOT NULL constraints to ensure referential integrity (dropping orphaned reviews) and used SELECT DISTINCT to handle deduplication.
• Schema Generation: The Python engine executes the SQL transformations, automatically generating the finalized dimension and fact tables required for our BI data model.

Phase 3: The Final Artefacts (Power BI Import)
The output of the pipeline consists of four highly optimized CSV files that serve as the foundation for our Power BI dashboard:

• dim_listing.csv: Contains static property details (price, location, superhost status).
• dim_date.csv: Calendar table for time-series analysis and weekend vs. weekday grouping.
• fact_weather.csv: Daily meteorological readings (temps, rain, wind gusts).
• fact_reviews.csv: The core transactional table containing the continuous sentiment scores, isolated weather sentences, and targeted weather sentiment scores.

By separating the data into Dimensions and Facts, we ensure our BI tool can efficiently cross-filter massive amounts of data without performance degradation

