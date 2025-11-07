import ndjson
import pandas as pd
from pandas import json_normalize
import os
import re
from pathlib import Path


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
        'data.caption.text',          # text of the post
        'data.caption.created_at',    # post creation time
        'data.media_type',            # image, video, carousel
        'data.permalink',             # full URL to post
        'data.like_count',
        'data.comment_count',
        'data.ig_play_count',
        'data.username',
        'data.media_url',             # direct media link
        'data.children.data',         # if carousel
    ]

    # Filter existing columns
    available_cols = [c for c in columns_to_select if c in df_flat.columns]
    df_small = df_flat.loc[:, available_cols]

    # Convert timestamp to datetime
    if (
            "data.caption.created_at" in df_small.columns
            or "data.taken_at" in df_small.columns
            or "timestamp_collected" in df_small.columns
    ):
        # 0) Coalesce without .fillna(None) — use combine_first or a Series default
        s_empty = pd.Series(index=df_small.index, dtype="float64")
        cap = df_small.get("data.caption.created_at", s_empty)
        taken = df_small.get("data.taken_at", s_empty)
        coll = df_small.get("timestamp_collected", s_empty)

        merged = cap.combine_first(taken).combine_first(coll)
        df_small["data.caption.created_at"] = merged

        raw_series = df_small["data.caption.created_at"]

        # 1) Numeric epochs FIRST (handles floats like 1.757675626e9)
        numeric = pd.to_numeric(raw_series, errors="coerce")
        dt_col = pd.Series(pd.NaT, index=raw_series.index, dtype="datetime64[ns, UTC]")

        s_mask = numeric.notna() & (numeric < 1e11)  # seconds
        ms_mask = numeric.notna() & (numeric >= 1e11) & (numeric < 1e14)  # ms
        us_mask = numeric.notna() & (numeric >= 1e14) & (numeric < 1e17)  # µs
        ns_mask = numeric.notna() & (numeric >= 1e17)  # ns

        if s_mask.any():
            dt_col.loc[s_mask] = pd.to_datetime(numeric[s_mask], unit="s", utc=True, errors="coerce")
        if ms_mask.any():
            dt_col.loc[ms_mask] = pd.to_datetime(numeric[ms_mask], unit="ms", utc=True, errors="coerce")
        if us_mask.any():
            dt_col.loc[us_mask] = pd.to_datetime(numeric[us_mask], unit="us", utc=True, errors="coerce")
        if ns_mask.any():
            dt_col.loc[ns_mask] = pd.to_datetime(numeric[ns_mask], unit="ns", utc=True, errors="coerce")

        # 2) Remaining strings (ISO first, then flexible)
        still_na = dt_col.isna()
        if still_na.any():
            raw_str = raw_series.astype("string").str.strip()
            is_digits = raw_str.str.fullmatch(r"\d+")
            iso_try = pd.to_datetime(raw_str.where(~is_digits, None), errors="coerce", utc=True, format="ISO8601")
            dt_col.loc[still_na & iso_try.notna()] = iso_try[still_na & iso_try.notna()]
            need_fallback = still_na & ~is_digits & raw_str.notna() & (raw_str != "")
            if need_fallback.any():
                dt_col.loc[need_fallback] = pd.to_datetime(raw_str[need_fallback], errors="coerce", utc=True)

        df_small["data.caption.created_at"] = dt_col

        # Date filter (UTC-aware; include whole end day if no time given)
        date_a = pd.to_datetime(date_a, utc=True, errors="coerce")
        date_b = pd.to_datetime(date_b, utc=True, errors="coerce")
        if pd.notna(date_b) and date_b.time() == pd.Timestamp(0, tz="UTC").time():
            date_b = date_b + pd.Timedelta(days=1) - pd.Timedelta(microseconds=1)

        df_small = df_small[
            (df_small["data.caption.created_at"] >= date_a) &
            (df_small["data.caption.created_at"] <= date_b)
            ]

    return df_small


### Clean files

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent  # adjusted to reach the root directory

raw_dir = PROJECT_ROOT / "A_Data" / "2_Instagram" / "1_RAW"
clean_dir = PROJECT_ROOT / "A_Data" / "2_Instagram" / "2_CLEAN"

os.makedirs(clean_dir, exist_ok=True)

for file in os.listdir(raw_dir):
    filename = os.fsdecode(file)
    file_path = os.path.join(raw_dir, filename)

    print(f"Processing {filename}...")

    return_df = prepinstagram_through_user(file_path, "2025-03-09", "2025-10-12")

    # If nothing survived the filter, skip writing an empty CSV
    if return_df is None or return_df.empty:
        print(f"[WARN] No rows after filtering for {filename}. Skipping save.")
        continue

    # Clean only the caption text to avoid multi-line CSV rows
    if "data.caption.text" in return_df.columns:
        return_df["data.caption.text"] = (
            return_df["data.caption.text"]
            .astype(str)
            .apply(lambda x: re.sub(r'[\r\n]+', ' ', x))
        )

    save_path = os.path.join(clean_dir, filename.split('Instagram')[0] + "_cleaned.csv")
    return_df.to_csv(save_path, index=False)

print("✅ All done!")
