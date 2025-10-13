import ndjson
import pandas as pd
from pandas import json_normalize
import os

def prepinstagram_through_user(file_name, date_a, date_b):
    # Load NDJSON file
    with open(file_name, 'r') as f:
        data = ndjson.load(f)

    # Flatten nested JSON
    df_flat = json_normalize(data)

    # Adjust columns to Instagram structure (you may adapt based on your actual schema)
    columns_to_select = [
        'source_platform',
        'source_platform_url',
        'user.username',
        'data.id',
        'data.caption.text',             # text of the post
        'data.timestamp',           # post creation time
        'data.media_type',          # image, video, carousel
        'data.permalink',           # full URL to post
        'data.like_count',
        'data.comment_count',
        'data.ig_play_count',
        'data.username',
        'data.media_url',           # direct media link
        'data.children.data',       # if carousel
    ]

    # Filter existing columns
    available_cols = [c for c in columns_to_select if c in df_flat.columns]
    df_small = df_flat.loc[:, available_cols]

    # Convert timestamp to datetime
    if 'data.timestamp' in df_small.columns:
        df_small['data.timestamp'] = pd.to_datetime(df_small['data.timestamp'], errors='coerce')

        # Date filter
        date_a = pd.to_datetime(date_a)
        date_b = pd.to_datetime(date_b)
        df_small = df_small[
            (df_small['data.timestamp'] >= date_a) & (df_small['data.timestamp'] <= date_b)
        ]

    return df_small


### Clean files

raw_dir = "/Users/nickeichmann/PythonProjects/Introduction-to-Computational-Media-Research/A_Data/2_Instagram/1_RAW"
clean_dir = "/Users/nickeichmann/PythonProjects/Introduction-to-Computational-Media-Research/A_Data/2_Instagram/2_CLEAN"

os.makedirs(clean_dir, exist_ok=True)

for file in os.listdir(raw_dir):
    filename = os.fsdecode(file)
    file_path = os.path.join(raw_dir, filename)

    print(f"Processing {filename}...")

    return_df = prepinstagram_through_user(file_path, "2025-03-09", "2025-10-12")

    save_path = os.path.join(clean_dir, filename.split('Instagram')[0] + "_cleaned.csv")
    return_df.to_csv(save_path, index=False)

print("✅ All done!")
