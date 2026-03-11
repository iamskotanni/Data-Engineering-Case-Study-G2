import pandas as pd

# Load data
listings = pd.read_csv('listings.csv')
# reviews = pd.read_csv('reviews.csv')
reviews = pd.read_csv('reviews.csv', usecols=['listing_id', 'date'])
weather = pd.read_csv('capetown_weather.csv')


# Convert dates
reviews["date"]=pd.to_datetime(reviews["date"], dayfirst=True, errors='coerce')



reviews_march=reviews[
    (reviews["date"]>="2024-03-01") &
    (reviews["date"]<="2024-03-31")
]
weather['date'] = pd.to_datetime(weather['date'], dayfirst=True, errors='coerce')

# Merge reviews with weather
reviews_weather = pd.merge(reviews_march, weather, on='date', how='left')

# Merge with listings
full_data = pd.merge(reviews_weather, listings, left_on='listing_id', right_on='id', how='left')
# print(full_data.head())
# print(full_data.shape)

full_data.to_csv("Full_data_r2.csv", index=False)