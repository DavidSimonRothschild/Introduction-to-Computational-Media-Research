import os
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

import matplotlib.pyplot as plt

from scipy.stats import pearsonr

import seaborn as sns

# ---- paths ----
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
input_csv = PROJECT_ROOT / "A_Data" / "2_Instagram" / "2_CLEAN"

TEXT_COLUMN = "data.caption.text"
SENTIMENT_COLUMN = "sentiment_rulebased"


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


# ---- 1) Load all Insta CSVs into one DataFrame with party column ----
dfs = []

for filename in os.listdir(input_csv):
    if not filename.endswith(".csv"):
        continue

    filepath = input_csv / filename
    df = pd.read_csv(filepath)

    if SENTIMENT_COLUMN not in df.columns:
        print(f"Skipping {filename}: '{SENTIMENT_COLUMN}' not found.")
        continue

    party = infer_party_from_filename(filename)
    df["party"] = party

    dfs.append(df)

insta_all = pd.concat(dfs, ignore_index=True)

# Optional sanity check
print(insta_all[["party", SENTIMENT_COLUMN]].head())


# ---- 2) Mean comparison / descriptives per party (kept in memory) ----
party_summary = (
    insta_all
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

insta_all.boxplot(
    column=SENTIMENT_COLUMN,
    by="party",
)

plt.axhline(0, linestyle="--", linewidth=1)  # neutral line
plt.title("Sentiment distribution by party (Instagram captions)")
plt.suptitle("")  # remove pandas' default suptitle
plt.xlabel("Party")
plt.ylabel("Rule-based sentiment")
plt.tight_layout()
plt.show()

#################
#Correlation
#################
SENTIMENT_COLUMN = "sentiment_rulebased"

# 1) Load follower table
followers_path = Path(
    "/Users/nickeichmann/PythonProjects/Introduction-to-Computational-Media-Research/A_Data/partei_tabelle.csv"
)

followers_df = pd.read_csv(followers_path)  # comma-separated in your example

print("Follower table columns:", followers_df.columns.tolist())
# ['Index', 'Partei', 'Link-Instagram', 'Link-Tiktok', 'Follower-Instagram', 'Follower-Tiktok']

# 2) Keep only needed columns + normalize party names to match insta_all
followers_df = followers_df[["Partei", "Follower-Instagram"]].copy()

# map 'Partei' values to the party codes used in insta_all
party_map = {
    # Mother parties
    "SVP": "SVP",
    "SP": "SP",
    "FDP": "FDP",
    "Die Mitte": "Mitte",
    "Grüne": "Gruene",
    "GLP": "GLP",
    "EVP": "EVP",

    # Youth wings – adapt to how they appear in your insta_all["party"]
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
followers_df = followers_df.rename(columns={"Follower-Instagram": "followers_instagram"})

print(followers_df)

# 3) Merge onto insta_all by 'party'
insta_all = insta_all.merge(
    followers_df[["party", "followers_instagram"]],
    on="party",
    how="left",
)


insta_cut = insta_all[insta_all["data.like_count"] <= 2000].copy()

insta_cut["likes_per_follower"] = (
    insta_cut["data.like_count"] / insta_cut["followers_instagram"]
)

# 5) Build correlation matrix between sentiment, raw likes, and likes_per_follower
insta_corr = insta_cut[
    [SENTIMENT_COLUMN, "data.like_count", "likes_per_follower"]
].dropna()

corr_matrix = insta_corr.corr(method="pearson")
print("\nCorrelation matrix:")
print(corr_matrix)

import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid", font_scale=1.1)

# we only have 2 pairs, so (1, 2), not (1, 3)
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

pairs = [
    ("sentiment_rulebased", "data.like_count"),
    ("sentiment_rulebased", "likes_per_follower"),
]

for ax, (x, y) in zip(axes, pairs):
    sns.regplot(
        data=insta_corr,
        x=x,
        y=y,
        ax=ax,
        scatter_kws={"alpha": 0.5, "s": 20},
        line_kws={"color": "black"},
    )

    # Compute Pearson correlation coefficient and p-value
    x_vals = insta_corr[x]
    y_vals = insta_corr[y]
    alpha, p_val = pearsonr(x_vals, y_vals)

    x_label = x.replace("_", " ")
    y_label = y.replace("_", " ")

    ax.set_title(f"{x_label} vs {y_label}\nα = {alpha:.3f}, p = {p_val:.3g}", fontsize=12)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

plt.tight_layout()
plt.show()