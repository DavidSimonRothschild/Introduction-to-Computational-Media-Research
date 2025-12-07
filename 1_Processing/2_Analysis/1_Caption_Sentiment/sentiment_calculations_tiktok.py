import os
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from scipy.stats import pearsonr

# ---- paths ----
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
input_csv = PROJECT_ROOT / "A_Data" / "1_Tiktok" / "2_CLEAN"

TEXT_COLUMN = "data.desc"
SENTIMENT_COLUMN = "sentiment_rulebased"

# adjust this to your actual likes column in the TikTok CSVs
LIKE_COLUMN = "data.stats.diggCount"  # e.g. "data.digg_count" / "data.stats.diggCount" etc.


def infer_party_from_filename(filename: str) -> str:
    """
    Infer party name from a filename like
    '12_Junge_Gruene__cleaned.csv' -> 'Junge_Gruene'
    'SVP__cleaned.csv'             -> 'SVP'
    Adjust this if your pattern differs.
    """
    base = filename.rsplit(".csv", 1)[0]      # drop extension
    base = base.split("__")[0]                # drop suffix like '__cleaned'
    parts = base.split("_")
    if parts[0].isdigit():
        party = "_".join(parts[1:])           # drop leading index
    else:
        party = base
    return party


# ---- 1) Load all TikTok CSVs into one DataFrame with party column ----
dfs = []

for filename in os.listdir(input_csv):
    if not filename.endswith(".csv"):
        continue

    filepath = input_csv / filename
    df = pd.read_csv(filepath)

    if SENTIMENT_COLUMN not in df.columns:
        print(f"Skipping {filename}: '{SENTIMENT_COLUMN}' not found.")
        continue

    if LIKE_COLUMN not in df.columns:
        print(f"WARNING: {filename} has no '{LIKE_COLUMN}' column. Available columns:")
        print(df.columns.tolist())
        continue

    party = infer_party_from_filename(filename)
    df["party"] = party

    dfs.append(df)

tiktok_all = pd.concat(dfs, ignore_index=True)

# Optional sanity check
print(tiktok_all[["party", SENTIMENT_COLUMN, LIKE_COLUMN]].head())


# ---- 2) Mean comparison / descriptives per party (kept in memory) ----
party_summary = (
    tiktok_all
    .groupby("party")[SENTIMENT_COLUMN]
    .agg(
        n      = "count",
        mean   = "mean",
        median = "median",
        std    = "std",
        min    = "min",
        p25    = lambda x: x.quantile(0.25),
        p75    = lambda x: x.quantile(0.75),
        max    = "max",
    )
    .sort_values("mean", ascending=False)
)

print(party_summary)


# ---- 3) Boxplots of sentiment per party ----
plt.figure(figsize=(10, 5))

tiktok_all.boxplot(
    column=SENTIMENT_COLUMN,
    by="party",
)

plt.axhline(0, linestyle="--", linewidth=1)  # neutral line
plt.title("Sentiment distribution by party (TikTok captions)")
plt.suptitle("")  # remove pandas' default suptitle
plt.xlabel("Party")
plt.ylabel("Rule-based sentiment")
plt.tight_layout()
plt.show()

#################
# Correlation
#################

# 1) Load follower table
followers_path = PROJECT_ROOT / "A_Data" / "partei_tabelle.csv"
followers_df = pd.read_csv(followers_path)

# Clean column names
followers_df.columns = followers_df.columns.str.strip()
print("Follower table columns:", followers_df.columns.tolist())
# ['Index', 'Partei', 'Link-Instagram', 'Link-Tiktok', 'Follower-Instagram', 'Follower-Tiktok']

# 2) Keep only needed columns + normalize party names to match tiktok_all
followers_df = followers_df[["Partei", "Follower-Tiktok"]].copy()

# strip whitespace in Partei values too
followers_df["Partei"] = followers_df["Partei"].astype(str).str.strip()

# map 'Partei' values to the party codes used in tiktok_all
party_map = {
    # Mother parties
    "SVP": "SVP",
    "SP": "SP",
    "FDP": "FDP",
    "Die Mitte": "Mitte",
    "Grüne": "Gruene",
    "GLP": "GLP",
    "EVP": "EVP",

    # Youth wings – adapt to how they appear in your tiktok_all["party"]
    "JSVP": "JSVP",
    "JUSO": "JUSO",
    "JF": "JF",  # Jungfreisinnige
    "Die Junge Mitte": "Junge_Mitte",
    "Junge Grüne": "Junge_Gruene",
    "Junge GLP": "Junge_GLP",
    "Junge EVP": "Junge_EVP",
}

followers_df["party"] = followers_df["Partei"].map(party_map)

# drop rows where we don't have a mapping (just in case)
followers_df = followers_df.dropna(subset=["party"])

# rename followers column
followers_df = followers_df.rename(columns={"Follower-Tiktok": "followers_tiktok"})

print(followers_df)

# 3) Merge onto tiktok_all by 'party'
tiktok_all = tiktok_all.merge(
    followers_df[["party", "followers_tiktok"]],
    on="party",
    how="left",
)

# 4) Apply cutoff at 2000 likes and compute likes_per_follower
tiktok_cut = tiktok_all[tiktok_all[LIKE_COLUMN] <= 2000].copy()

tiktok_cut["likes_per_follower"] = (
    tiktok_cut[LIKE_COLUMN] / tiktok_cut["followers_tiktok"]
)

# 5) Build correlation matrix between sentiment, raw likes, and likes_per_follower
tiktok_corr = tiktok_cut[
    [SENTIMENT_COLUMN, LIKE_COLUMN, "likes_per_follower"]
].dropna()

corr_matrix = tiktok_corr.corr(method="pearson")
print("\nCorrelation matrix (TikTok, likes ≤ 2000):")
print(corr_matrix)

# 6) Scatterplots with α annotated
sns.set(style="whitegrid", font_scale=1.1)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

pairs = [
    (SENTIMENT_COLUMN, LIKE_COLUMN),
    (SENTIMENT_COLUMN, "likes_per_follower"),
]

for ax, (x, y) in zip(axes, pairs):
    sns.regplot(
        data=tiktok_corr,
        x=x,
        y=y,
        ax=ax,
        scatter_kws={"alpha": 0.5, "s": 20},
        line_kws={"color": "black"},
    )

    # Compute Pearson correlation coefficient and p-value
    x_vals = tiktok_corr[x]
    y_vals = tiktok_corr[y]
    alpha, p_val = pearsonr(x_vals, y_vals)

    # nicer labels
    x_label = x.replace("_", " ")
    y_label = y.replace("_", " ")

    ax.set_title(f"{x_label} vs {y_label}\nα = {alpha:.3f}, p = {p_val:.3g}", fontsize=12)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

plt.tight_layout()
plt.show()
