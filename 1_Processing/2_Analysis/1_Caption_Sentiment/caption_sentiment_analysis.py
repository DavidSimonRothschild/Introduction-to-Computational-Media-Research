from pathlib import Path
import pandas as pd
from germansentiment import SentimentModel

# 1) project root = folder where this script sits (adjust if needed)
# if this file is in e.g. scripts/sentiment.py and your data is in A_Data/..., go up one level
PROJECT_ROOT = Path(__file__).resolve().parent.parent  # adjust .parent/.parent as needed

# 2) define input/output relative to project root
input_csv = PROJECT_ROOT / "A_Data" / "2_Instagram" / "2_CLEAN" / "1_SVP__cleaned.csv"
output_csv = PROJECT_ROOT / "A_Data" / "2_Instagram" / "2_CLEAN" / "1_SVP__cleaned_with_sentiment.csv"

# 3) load model
model = SentimentModel()

# 4) read data
df = pd.read_csv(input_csv)

# 5) pick the column to analyze
col = "data.caption.text"
texts = df[col].fillna("").tolist()

# 6) run sentiment
sentiments = model.predict_sentiment(texts)

# 7) attach to dataframe
df["sentiment"] = sentiments

# 8) save
df.to_csv(output_csv, index=False)
print(f"Saved to {output_csv}")
