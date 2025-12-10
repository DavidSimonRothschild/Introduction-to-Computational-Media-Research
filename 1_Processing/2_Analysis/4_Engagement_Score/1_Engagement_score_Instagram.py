from pathlib import Path
import os
import pandas as pd


# ------------ CONFIG ------------ #

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent

# Folder with your party-level CSVs
INPUT_FOLDER = PROJECT_ROOT / "A_Data" / "2_Instagram" / "2_CLEAN"

LIKE_COL = "data.like_count"
COMMENT_COL = "data.comment_count"
ENGAGEMENT_COL = "engagement_score"   # final, mean-centered


# ------------ CORE LOGIC ------------ #

def add_engagement_score(
    df: pd.DataFrame,
    like_col: str = LIKE_COL,
    comment_col: str = COMMENT_COL,
    out_col: str = ENGAGEMENT_COL,
) -> pd.DataFrame:
    """
    For one DataFrame (one party CSV):

    Step 1 (raw score):
        raw_i = (likes_i / avg_likes) + (comments_i / avg_comments)

    Step 2 (centered):
        engagement_score_i = raw_i - mean(raw_i)   # mean 0 per CSV
    """

    # ensure numeric
    df[like_col] = pd.to_numeric(df[like_col], errors="coerce")
    df[comment_col] = pd.to_numeric(df[comment_col], errors="coerce")

    avg_likes = df[like_col].mean(skipna=True)
    avg_comments = df[comment_col].mean(skipna=True)

    def compute_raw_row(row):
        likes = row[like_col]
        comments = row[comment_col]

        part_likes = 0.0
        part_comments = 0.0

        if pd.notna(likes) and pd.notna(avg_likes) and avg_likes != 0:
            part_likes = likes / avg_likes

        if pd.notna(comments) and pd.notna(avg_comments) and avg_comments != 0:
            part_comments = comments / avg_comments

        return part_likes + part_comments

    # Step 1: raw engagement score
    df["_engagement_raw"] = df.apply(compute_raw_row, axis=1)

    # Step 2: center to mean 0 within this CSV
    mean_raw = df["_engagement_raw"].mean(skipna=True)
    df[out_col] = df["_engagement_raw"] - mean_raw

    # drop helper column
    df = df.drop(columns=["_engagement_raw"])

    return df


def process_folder(input_folder: Path):
    """
    Go through all CSVs in the folder, compute mean-centered engagement_score per CSV,
    and overwrite the files.
    """
    for filename in os.listdir(input_folder):
        if not filename.endswith(".csv"):
            continue

        filepath = input_folder / filename
        print(f"Processing {filepath} ...")

        df = pd.read_csv(filepath)

        # check that the needed columns exist
        if LIKE_COL not in df.columns or COMMENT_COL not in df.columns:
            print(f"  Missing {LIKE_COL} or {COMMENT_COL} in {filename}, skipping.")
            continue

        df = add_engagement_score(df, LIKE_COL, COMMENT_COL, ENGAGEMENT_COL)

        df.to_csv(filepath, index=False)
        print(f"  Saved with {ENGAGEMENT_COL} (mean-centered) to {filepath}")


if __name__ == "__main__":
    process_folder(INPUT_FOLDER)
