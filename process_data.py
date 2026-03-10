import pandas as pd
from transformers import pipeline
print("1. Loading the FULL DATA MERGED merged dataset...")
df = pd.read_csv("FULL DATA MERGED.csv")

print("2. Cleaning the price column...")
if 'price' in df.columns:
   # Remove the dollar sign and commas, then convert to a usable float number
   df['price'] = df['price'].astype(str).str.replace('$', '', regex=False).str.replace(',', '', regex=False)
   df['price'] = pd.to_numeric(df['price'], errors='coerce')

print("3. Downloading and initializing the Hugging Face AI Model...")
# Adding top_k=None forces the model to give us the probabilities for ALL 5 star categories
sentiment_pipeline = pipeline(
   "sentiment-analysis",
   model="nlptown/bert-base-multilingual-uncased-sentiment",
   truncation=True,
   max_length=512,
   top_k=None
)
def get_granular_star_rating(text):
   if pd.isna(text) or str(text).strip() == "":
       return None
   try:
       # The model now outputs a list of all 5 probabilities
       results = sentiment_pipeline(str(text))[0]
       expected_stars = 0.0
       # Loop through the probabilities and apply our weighted formula
       for res in results:
           # Extract the integer star value (e.g., '4' from '4 stars')
           star_val = int(res['label'].split()[0])
           # The probability score (e.g., 0.85)
           prob = res['score']
           # Multiply and add to our total
           expected_stars += (star_val * prob)
       # Round it to 2 decimal places (e.g., 4.82)
       return round(expected_stars, 2)
   except Exception as e:
       return None
   
print("4. Analyzing reviews for  granular 1-5 Star Sentiment (This may take a few minutes)...")
# Apply our new granular function to the comments column
df['sentiment_stars'] = df['comments'].apply(get_granular_star_rating)

print("5. Throwing away the junk columns...")
# These are our "Keepers" for the Star Schema
columns_to_keep = [
   'listing_id', 'id_x', 'date', 'temp_max', 'temp_min', 'apparent_temp_max',
   'apparent_temp_min', 'rain', 'wind_speed', 'wind_gust', 'humidity',
   'neighbourhood_cleansed', 'property_type', 'room_type', 'host_is_superhost',
   'price', 'sentiment_stars'
]
# Safety check: Keep only the columns that actually exist in the dataframe
actual_columns_to_keep = [col for col in columns_to_keep if col in df.columns]
df_clean = df[actual_columns_to_keep]
# Drop any rows where we couldn't calculate a sentiment
df_clean = df_clean.dropna(subset=['sentiment_stars'])

print("6. Saving the highly granular dataset...")

df_clean.to_csv("CLEANED_DATA_V2.csv", index=False)
print("SUCCESS! CLEANED_DATA_V2.csv is ready for the database.")