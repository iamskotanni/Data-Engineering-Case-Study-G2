import duckdb
import pandas as pd
print("1. Loading CLEANED_DATA_V2.csv into memory as the 'staging_table'...")
# DuckDB will automatically see this pandas dataframe when the SQL runs
staging_table = pd.read_csv('CLEANED_DATA_V2.csv')

print("2. Spinning up the local database (airbnb_data.db)...")

# This creates a real database file in the folder
con = duckdb.connect('airbnb_data.db')
print("3. Reading your transformations.sql script...")
with open('transformations.sql', 'r') as file:
   sql_script = file.read()

print("4. Executing the DDL and DML (Building the Star Schema)...")
# This runs the SQL code against the dataframe and builds the 4 tables
con.execute(sql_script)
print("5. Exporting the beautiful, organized tables for Power BI...")
# Power BI loves having the Dimension and Fact tables as separate CSVs

con.execute("COPY dim_listing TO 'dim_listing.csv' (HEADER, DELIMITER ',')")
con.execute("COPY dim_date TO 'dim_date.csv' (HEADER, DELIMITER ',')")
con.execute("COPY fact_weather TO 'fact_weather.csv' (HEADER, DELIMITER ',')")
con.execute("COPY fact_reviews TO 'fact_reviews.csv' (HEADER, DELIMITER ',')")
print("SUCCESS! Data architecture is complete.")
con.close()