import ndjson
import pandas as pd
from pandas import json_normalize
import os
import re

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
        'data.caption.created_at',           # post creation time
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
    if "data.caption.created_at" in df_small.columns:
        raw = df_small["data.caption.created_at"].astype("string").str.strip()
        is_digits = raw.str.fullmatch(r"\d+")

        # Parse non-digits (ISO, RFC, etc.)
        dt_col = pd.to_datetime(raw.where(~is_digits, None), errors="coerce", utc=True)

        # Parse pure-digit epochs by length
        nums = pd.to_numeric(raw.where(is_digits, None), errors="coerce")
        lens = raw.str.len()

        mask_s = is_digits & (lens == 10)  # seconds
        mask_ms = is_digits & (lens == 13)  # milliseconds
        mask_us = is_digits & (lens == 16)  # microseconds
        mask_ns = is_digits & (lens >= 19)  # nanoseconds (very long)

        if mask_s.any():
            dt_col.loc[mask_s] = pd.to_datetime(nums[mask_s], unit="s", errors="coerce", utc=True)
        if mask_ms.any():
            dt_col.loc[mask_ms] = pd.to_datetime(nums[mask_ms], unit="ms", errors="coerce", utc=True)
        if mask_us.any():
            dt_col.loc[mask_us] = pd.to_datetime(nums[mask_us], unit="us", errors="coerce", utc=True)
        if mask_ns.any():
            dt_col.loc[mask_ns] = pd.to_datetime(nums[mask_ns], unit="ns", errors="coerce", utc=True)

        df_small["data.caption.created_at"] = dt_col

        # Date filter
        date_a = pd.to_datetime(date_a, utc=True, errors="coerce")
        date_b = pd.to_datetime(date_b, utc=True, errors="coerce")

        df_small = df_small[
            (df_small["data.caption.created_at"] >= date_a) &
            (df_small["data.caption.created_at"] <= date_b)
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

    # 🔹 Clean only the caption text to avoid multi-line CSV rows
    if "data.caption.text" in return_df.columns:
        return_df["data.caption.text"] = (
            return_df["data.caption.text"]
            .astype(str)
            .apply(lambda x: re.sub(r'[\r\n]+', ' ', x))
        )

    save_path = os.path.join(clean_dir, filename.split('Instagram')[0] + "_cleaned.csv")
    return_df.to_csv(save_path, index=False)

print("✅ All done!")
