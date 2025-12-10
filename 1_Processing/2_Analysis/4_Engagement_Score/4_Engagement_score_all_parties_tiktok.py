from pathlib import Path
import os
import pandas as pd


# ------------ CONFIG ------------ #

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
INPUT_FOLDER = PROJECT_ROOT / "A_Data" / "1_Tiktok" / "2_CLEAN"

LIKE_COL = "data.stats.diggCount"       # likes
COMMENT_COL = "data.stats.commentCount" # comments
SHARE_COL = "data.stats.shareCount"     # shares
VIEW_COL = "data.stats.playCount"       # views


# ------------ HELPERS ------------ #

def infer_party_from_filename(filename: str) -> str:
    """
    Infer party name from a filename like
    '12_Junge_Gruene__cleaned.csv' -> 'Junge_Gruene'
    'SP__cleaned.csv'              -> 'SP'
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

def build_tiktok_party_engagement_summary(input_folder: Path) -> pd.DataFrame:
    """
    For each party (CSV file), compute:
      - total likes
      - total comments
      - total shares
      - total views
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

        needed = [LIKE_COL, COMMENT_COL, SHARE_COL, VIEW_COL]
        if not all(col in df.columns for col in needed):
            print(f"  Missing one of {needed} in {filename}, skipping.")
            continue

        # ensure numeric
        for col in needed:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        total_likes = df[LIKE_COL].sum(skipna=True)
        total_comments = df[COMMENT_COL].sum(skipna=True)
        total_shares = df[SHARE_COL].sum(skipna=True)
        total_views = df[VIEW_COL].sum(skipna=True)
        n_posts = len(df)

        rows.append(
            {
                "party": party,
                "total_likes": total_likes,
                "total_comments": total_comments,
                "total_shares": total_shares,
                "total_views": total_views,
                "n_posts": n_posts,
            }
        )

    summary = pd.DataFrame(rows)

    if summary.empty:
        print("No valid CSVs found, summary is empty.")
        return summary

    # averages across parties (for totals)
    avg_total_likes = summary["total_likes"].mean(skipna=True)
    avg_total_comments = summary["total_comments"].mean(skipna=True)
    avg_total_shares = summary["total_shares"].mean(skipna=True)
    avg_total_views = summary["total_views"].mean(skipna=True)

    # raw indices relative to all-party averages
    summary["likes_index_raw"] = summary["total_likes"] / avg_total_likes
    summary["comments_index_raw"] = summary["total_comments"] / avg_total_comments
    summary["shares_index_raw"] = summary["total_shares"] / avg_total_shares
    summary["views_index_raw"] = summary["total_views"] / avg_total_views

    # combined raw engagement index (simple sum of the four indices)
    summary["engagement_index_raw"] = (
        summary["likes_index_raw"]
        + summary["comments_index_raw"]
        + summary["shares_index_raw"]
        + summary["views_index_raw"]
    )

    # ---- mean-center indices (zero-centered) ----
    summary["likes_index_centered"] = (
        summary["likes_index_raw"] - summary["likes_index_raw"].mean(skipna=True)
    )
    summary["comments_index_centered"] = (
        summary["comments_index_raw"] - summary["comments_index_raw"].mean(skipna=True)
    )
    summary["shares_index_centered"] = (
        summary["shares_index_raw"] - summary["shares_index_raw"].mean(skipna=True)
    )
    summary["views_index_centered"] = (
        summary["views_index_raw"] - summary["views_index_raw"].mean(skipna=True)
    )
    summary["engagement_index_centered"] = (
        summary["engagement_index_raw"]
        - summary["engagement_index_raw"].mean(skipna=True)
    )

    return summary


if __name__ == "__main__":
    summary_df = build_tiktok_party_engagement_summary(INPUT_FOLDER)
    # e.g. sort by centered engagement index
    print(summary_df.sort_values("engagement_index_centered", ascending=False))
