import pandas as pd
import re
from transformers import pipeline
print("1. Loading the massive merged dataset...")
df = pd.read_csv("FULL DATA MERGED.csv")
print("2. Cleaning the price column...")
if 'price' in df.columns:
   df['price'] = df['price'].astype(str).str.replace('$', '', regex=False).str.replace(',', '', regex=False)
   df['price'] = pd.to_numeric(df['price'], errors='coerce')
print("3. Downloading and initializing the Hugging Face AI Model...")
# Using your exact working parameters + top_k=None for granular probabilities
sentiment_pipeline = pipeline(
   "sentiment-analysis",
   model="nlptown/bert-base-multilingual-uncased-sentiment",
   truncation=True,
   max_length=512,
   top_k=None
)
print("4. Prepping the Weather Mega-Dictionaries...")
patterns = {
   'Rain': r'\b(rain|rained|raining|rainy|drizzle|drizzled|drizzly|downpour|pouring|poured|storm|storms|stormy|storming|wet|leak|leaking|leaked|flood|flooded|flooding)\b',
   'Wind': r'\b(wind|winds|windy|windier|howl|howling|howled|gust|gusts|gusty|gusting|breeze|breezy|gale|gales|draft|drafty)\b',
   'Heat': r'\b(hot|hotter|hottest|heat|heating|heatwave|warmer|warmest|humid|humidity|sweat|sweating|sweaty|boil|boiling|stifling)\b',
   'Cold': r'\b(cold|colder|coldest|freeze|freezing|froze|frozen|chill|chilly|ice|icy|winter|wintery|drafty)\b'
}
# --- THE PROBABILITY MATH FUNCTION ---
def calculate_granular_score(ai_results):
   """Takes the 5 probabilities from the AI and calculates a precise decimal score."""
   expected_stars = 0.0
   for res in ai_results:
       star_val = int(res['label'].split()[0])
       prob = res['score']
       expected_stars += (star_val * prob)
   return round(expected_stars, 2)
# Ensure comments are strings and handle blanks safely
df['comments'] = df['comments'].fillna('').astype(str)
overall_scores = []
weather_categories = []
weather_sentences = []
weather_scores = []
total_rows = len(df)
print(f"5. Analyzing {total_rows} reviews for Overall & Weather Sentiment (This will take a few minutes!)...")
for index, row in df.iterrows():
   text_str = row['comments']
   # Skip completely empty rows
   if text_str.strip() == "":
       overall_scores.append(None)
       weather_categories.append(None)
       weather_sentences.append(None)
       weather_scores.append(None)
       continue
   text_lower = text_str.lower()
   # --- 1. OVERALL SENTIMENT (Granular) ---
   try:
       overall_res = sentiment_pipeline(text_str)[0]
       overall_score = calculate_granular_score(overall_res)
   except Exception:
       overall_score = None
   overall_scores.append(overall_score)
   # --- 2. ISOLATED WEATHER SENTIMENT (Granular) ---
   found_cat = None
   found_sent = None
   weather_score = None
   # Fast check: does a weather word exist anywhere in the text?
   if any(re.search(pat, text_lower) for pat in patterns.values()):
       # Split the review into individual sentences
       sentences = re.split(r'(?<=[.!?])\s+', text_str)
       for sentence in sentences:
           sentence_lower = sentence.lower()
           for category, pattern in patterns.items():
               if re.search(pattern, sentence_lower):
                   found_cat = category
                   found_sent = sentence.strip()
                   break
           if found_sent:
               break
       # Run AI exclusively on the extracted weather sentence
       if found_sent:
           try:
               weather_res = sentiment_pipeline(found_sent)[0]
               weather_score = calculate_granular_score(weather_res)
           except Exception:
               weather_score = None
   weather_categories.append(found_cat)
   weather_sentences.append(found_sent)
   weather_scores.append(weather_score)
   # Print progress every 1000 rows
   if index % 1000 == 0 and index > 0:
       print(f"   ...Processed {index} / {total_rows} rows...")
# Attach the new lists to the dataframe
df['sentiment_stars'] = overall_scores
df['weather_category'] = weather_categories
df['weather_sentence'] = weather_sentences
df['weather_sentiment_score'] = weather_scores
print("6. Throwing away the junk columns...")
# Note: I added the 3 new weather columns to your "keepers" list!
columns_to_keep = [
   'listing_id', 'id_x', 'date', 'temp_max', 'temp_min', 'apparent_temp_max',
   'apparent_temp_min', 'rain', 'wind_speed', 'wind_gust', 'humidity',
   'neighbourhood_cleansed', 'property_type', 'room_type', 'host_is_superhost',
   'price', 'sentiment_stars', 'weather_category', 'weather_sentence', 'weather_sentiment_score'
]
actual_columns_to_keep = [col for col in columns_to_keep if col in df.columns]
df_clean = df[actual_columns_to_keep]
# Drop any rows where we couldn't calculate an overall sentiment
df_clean = df_clean.dropna(subset=['sentiment_stars'])
print("7. Saving the highly accurate, granular dataset...")
df_clean.to_csv("CLEANED_DATA_V2.csv", index=False)
print("SUCCESS! CLEANED_DATA_V2.csv is ready for the database.")