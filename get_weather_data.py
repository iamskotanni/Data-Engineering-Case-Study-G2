import requests
import pandas as pd

latitude = -33.9258
longitude = 18.4232
url = "https://archive-api.open-meteo.com/v1/archive"
params = {
    "latitude": latitude,
    "longitude": longitude,
    "start_date": "2024-03-01",
    "end_date": "2024-03-31",
    "hourly": [
        "temperature_2m",
        "apparent_temperature",
        "precipitation",
        "windspeed_10m",
        "windgusts_10m",
        "relative_humidity_2m"
    ],
    "timezone": "auto"
}

response = requests.get(url, params=params)
data = response.json()

#print(data)

# Create DataFrame with 
hourly_df = pd.DataFrame({
    "time": data["hourly"]["time"],
    "temperature": data["hourly"]["temperature_2m"],
    "apparent_temperature": data["hourly"]["apparent_temperature"],
    "precipitation": data["hourly"]["precipitation"],
    "wind_speed": data["hourly"]["windspeed_10m"],
    "wind_gust": data["hourly"]["windgusts_10m"],
    "humidity": data["hourly"]["relative_humidity_2m"]
})

hourly_df["time"] = pd.to_datetime(hourly_df["time"])
hourly_df["date"] = hourly_df["time"].dt.date

#print(hourly_df)

# Aggregate to daily values
daily_weather = hourly_df.groupby("date").agg({
    "temperature": ["max", "min"],
    "apparent_temperature": ["max", "min"],
    "precipitation": "sum",
    "wind_speed": "max",
    "wind_gust": "max",
    "humidity": "mean"
}).reset_index()


# Flatten multi-level columns
daily_weather.columns = [
    'date',
    'temp_max', 'temp_min',
    'apparent_temp_max', 'apparent_temp_min',
    'rain',
    'wind_speed',
    'wind_gust',
    'humidity'
]
#print(daily_weather)

# Save to CSV
daily_weather.to_csv("capetown_weather.csv", index=False)


 
     
