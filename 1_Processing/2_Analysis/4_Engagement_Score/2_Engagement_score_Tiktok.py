from pathlib import Path
import os
import pandas as pd


# ------------ CONFIG ------------ #

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent

# Folder with your TikTok CSVs
INPUT_FOLDER = PROJECT_ROOT / "A_Data" / "1_Tiktok" / "2_CLEAN"

LIKE_COL = "data.stats.diggCount"       # likes
COMMENT_COL = "data.stats.commentCount" # comments
SHARE_COL = "data.stats.shareCount"     # shares
VIEW_COL = "data.stats.playCount"       # views

ENGAGEMENT_COL = "engagement_score"  # final, centered (mean = 0 per CSV)


# ------------ CORE LOGIC ------------ #

def add_engagement_score(
    df: pd.DataFrame,
    like_col: str = LIKE_COL,
    comment_col: str = COMMENT_COL,
    share_col: str = SHARE_COL,
    view_col: str = VIEW_COL,
    out_col: str = ENGAGEMENT_COL,
) -> pd.DataFrame:
    """
    For one DataFrame (one party's TikTok CSV):

    Step 1: raw_score_i =
        (likes_i   / avg_likes)   +
        (comments_i/ avg_comments)+
        (shares_i  / avg_shares)  +
        (views_i   / avg_views)

    Step 2: center to mean 0 in that CSV:
        engagement_score_i = raw_score_i - mean(raw_score)
    """

    # ensure numeric
    for col in [like_col, comment_col, share_col, view_col]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    avg_likes = df[like_col].mean(skipna=True)
    avg_comments = df[comment_col].mean(skipna=True)
    avg_shares = df[share_col].mean(skipna=True)
    avg_views = df[view_col].mean(skipna=True)

    def safe_part(value, avg):
        if pd.notna(value) and pd.notna(avg) and avg != 0:
            return value / avg
        return 0.0

    # Step 1: compute raw engagement score
    def compute_raw_row(row):
        likes = row[like_col]
        comments = row[comment_col]
        shares = row[share_col]
        views = row[view_col]

        part_likes = safe_part(likes, avg_likes)
        part_comments = safe_part(comments, avg_comments)
        part_shares = safe_part(shares, avg_shares)
        part_views = safe_part(views, avg_views)

        return part_likes + part_comments + part_shares + part_views

    df["_engagement_raw"] = df.apply(compute_raw_row, axis=1)

    # Step 2: center to mean 0 within this CSV
    mean_raw = df["_engagement_raw"].mean(skipna=True)
    df[out_col] = df["_engagement_raw"] - mean_raw

    # optionally drop helper column
    df = df.drop(columns=["_engagement_raw"])

    return df


def process_folder(input_folder: Path):
    """
    Go through all TikTok CSVs in the folder, compute centered engagement_score per CSV,
    and overwrite the files.
    """
    for filename in os.listdir(input_folder):
        if not filename.endswith(".csv"):
            continue

        filepath = input_folder / filename
        print(f"Processing {filepath} ...")

        df = pd.read_csv(filepath)

        needed = [LIKE_COL, COMMENT_COL, SHARE_COL, VIEW_COL]
        if not all(col in df.columns for col in needed):
            print(f"  Missing one of {needed} in {filename}, skipping.")
            continue

        df = add_engagement_score(df)

        df.to_csv(filepath, index=False)
        print(f"  Saved with {ENGAGEMENT_COL} (mean-centered) to {filepath}")


if __name__ == "__main__":
    process_folder(INPUT_FOLDER)
