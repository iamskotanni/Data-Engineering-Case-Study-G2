import pandas as pd
print("Loading both datasets into memory... (This might take a few seconds)")
df_raw = pd.read_csv('FULL DATA MERGED.csv')
df_clean = pd.read_csv('CLEANED_DATA_V2.csv')
# --- RAW DATA STATS ---
raw_total_rows = len(df_raw)
# Count how many rows actually had text in the comments column
raw_valid_comments = df_raw['comments'].notna().sum() if 'comments' in df_raw.columns else 0
# --- CLEAN DATA STATS ---
clean_total_rows = len(df_clean)
weather_mentions = df_clean['weather_category'].notna().sum()
avg_rating = df_clean['sentiment_stars'].mean()
# Calculate the drop-off
dropped_rows = raw_valid_comments - clean_total_rows
print("\n=== DATA PIPELINE SANITY CHECK ===")
print("1. THE RAW SOURCE (FULL DATA MERGED.csv)")
print(f"   - Total Rows in file: {raw_total_rows:,}")
print(f"   - Rows with actual text comments: {raw_valid_comments:,}")
print("\n2. THE FINAL OUTPUT (CLEANED_DATA_V2.csv)")
print(f"   - Total Successfully Scored Reviews: {clean_total_rows:,}")
print(f"   - Rows dropped during cleaning (blanks/errors): {dropped_rows:,}")
print("\n3. THE BUSINESS METRICS (For Slide 1)")
print(f"   - Explicit Weather Mentions: {weather_mentions:,}")
print(f"   - Average Overall Sentiment: {avg_rating:.2f} Stars")
