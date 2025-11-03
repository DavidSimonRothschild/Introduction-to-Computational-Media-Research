import pandas as pd
from germansentiment import SentimentModel

# 1) load model
model = SentimentModel()

# 2) load csv
df_path = "/Users/nickeichmann/PythonProjects/Introduction-to-Computational-Media-Research/A_Data/2_Instagram/2_CLEAN/1_SVP__cleaned.csv"
df = pd.read_csv(df_path)

# 3) pick the column to analyze
col = "data.caption.text"

# make sure there are no NaNs, convert to list
texts = df[col].fillna("").tolist()

# 4) run sentiment
sentiments = model.predict_sentiment(texts)

# 5) attach to dataframe
df["sentiment"] = sentiments

# 6) save (optional)
df.to_csv("/Users/nickeichmann/PythonProjects/Introduction-to-Computational-Media-Research/A_Data/2_Instagram/2_CLEAN/1_SVP__cleaned_with_sentiment.csv",
          index=False)
