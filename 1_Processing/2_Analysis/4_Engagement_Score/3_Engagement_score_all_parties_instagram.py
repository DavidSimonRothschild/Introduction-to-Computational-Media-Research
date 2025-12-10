from pathlib import Path
import os
import pandas as pd


# ------------ CONFIG ------------ #

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
INPUT_FOLDER = PROJECT_ROOT / "A_Data" / "2_Instagram" / "2_CLEAN"

LIKE_COL = "data.like_count"
COMMENT_COL = "data.comment_count"


# ------------ HELPERS ------------ #

def infer_party_from_filename(filename: str) -> str:
    """
    Infer party name from a filename like
    '12_Junge_Gruene__cleaned.csv' -> 'Junge_Gruene'
    'SVP__cleaned.csv'             -> 'SVP'
    Adjust if your pattern differs.
    """
    base = filename.rsplit(".csv", 1)[0]   # drop extension
    base = base.split("__")[0]             # drop suffix like '__cleaned'
    parts = base.split("_")
    if parts[0].isdigit():
        party = "_".join(parts[1:])        # drop leading index
    else:
        party = base
    return party


# ------------ CORE LOGIC ------------ #

def build_instagram_party_engagement_summary(input_folder: Path) -> pd.DataFrame:
    """
    For each party (CSV file), compute:
      - total likes
      - total comments
      - number of posts

    Then compute indices relative to the average across all parties and
    mean-center them so the average party has index 0.
    """

    rows = []

    for filename in os.listdir(input_folder):
        if not filename.endswith(".csv"):
            continue

        filepath = input_folder / filename
        party = infer_party_from_filename(filename)
        print(f"Processing {filepath} for party {party} ...")

        df = pd.read_csv(filepath)

        if LIKE_COL not in df.columns or COMMENT_COL not in df.columns:
            print(f"  Missing {LIKE_COL} or {COMMENT_COL} in {filename}, skipping.")
            continue

        # ensure numeric
        df[LIKE_COL] = pd.to_numeric(df[LIKE_COL], errors="coerce")
        df[COMMENT_COL] = pd.to_numeric(df[COMMENT_COL], errors="coerce")

        total_likes = df[LIKE_COL].sum(skipna=True)
        total_comments = df[COMMENT_COL].sum(skipna=True)
        n_posts = len(df)

        rows.append(
            {
                "party": party,
                "total_likes": total_likes,
                "total_comments": total_comments,
                "n_posts": n_posts,
            }
        )

    summary = pd.DataFrame(rows)

    if summary.empty:
        print("No valid CSVs found, summary is empty.")
        return summary

    # averages across parties
    avg_total_likes = summary["total_likes"].mean(skipna=True)
    avg_total_comments = summary["total_comments"].mean(skipna=True)

    # raw indices relative to all-party averages
    summary["likes_index_raw"] = summary["total_likes"] / avg_total_likes
    summary["comments_index_raw"] = summary["total_comments"] / avg_total_comments

    # combined raw index (e.g. simple sum)
    summary["engagement_index_raw"] = (
        summary["likes_index_raw"] + summary["comments_index_raw"]
    )

    # ---- mean-center indices (zero-centered) ----
    summary["likes_index_centered"] = (
        summary["likes_index_raw"] - summary["likes_index_raw"].mean(skipna=True)
    )
    summary["comments_index_centered"] = (
        summary["comments_index_raw"] - summary["comments_index_raw"].mean(skipna=True)
    )
    summary["engagement_index_centered"] = (
        summary["engagement_index_raw"]
        - summary["engagement_index_raw"].mean(skipna=True)
    )

    return summary


if __name__ == "__main__":
    summary_df = build_instagram_party_engagement_summary(INPUT_FOLDER)
    # e.g. sort by centered engagement index
    print(summary_df.sort_values("engagement_index_centered", ascending=False))
