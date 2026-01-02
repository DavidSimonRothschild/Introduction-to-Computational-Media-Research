import pandas as pd
import glob
import os
from pathlib import Path
from scipy.stats import mannwhitneyu
import numpy as np
import statsmodels.formula.api as smf


# ---------------- CONFIG ----------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
INSTAGRAM_FOLDER = PROJECT_ROOT / "A_Data" / "2_Instagram" / "2_CLEAN"
TIKTOK_FOLDER = PROJECT_ROOT / "A_Data" / "1_Tiktok" / "2_CLEAN"


# ---------------- LOAD DATA ----------------

def load_platform(path):
    files = glob.glob(os.path.join(path, "*.csv"))
    dfs = []
    for f in files:
        df = pd.read_csv(f)
        df["party_file"] = os.path.basename(f)
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True)

tiktok = load_platform(TIKTOK_FOLDER)
instagram = load_platform(INSTAGRAM_FOLDER)

tiktok["platform"] = "tiktok"
instagram["platform"] = "instagram"

df = pd.concat([tiktok, instagram], ignore_index=True)

df = df.dropna(subset=["engagement_score", "voting.topic"])


# ---------------- VOTING CATEGORIES ----------------

df["voting_cat"] = df["voting.topic"].map({
    0: "none",
    1: "eid_only",
    2: "eigenmietwert_only",
    3: "both"
})


# ---------------- DESCRIPTIVES ----------------

print("\n--- Descriptive statistics by voting category ---")
print(df.groupby("voting_cat")["engagement_score"].describe())


print("\n--- Combined voting (1,2,3) vs non-voting (0) ---")

df["is_any_voting"] = (df["voting.topic"] > 0).astype(int)

voting_all = df.loc[df.is_any_voting == 1, "engagement_score"]
non_voting = df.loc[df.is_any_voting == 0, "engagement_score"]

u, pval = mannwhitneyu(voting_all, non_voting, alternative="greater")

print("Mann-Whitney U p-value (any voting vs none):", pval)

med_v = voting_all.median()
med_nv = non_voting.median()

print("Median engagement – any voting:", med_v)
print("Median engagement – non voting:", med_nv)
print("Median shift (any voting – none):", med_v - med_nv)

print("\n--- Platform comparison: voting vs non-voting ---")

for p in ["instagram", "tiktok"]:
    sub = df[df.platform == p]

    voting = sub.loc[sub.is_any_voting == 1, "engagement_score"]
    non_voting = sub.loc[sub.is_any_voting == 0, "engagement_score"]

    u, pval = mannwhitneyu(voting, non_voting, alternative="greater")

    med_v = voting.median()
    med_nv = non_voting.median()

    print(f"\nPlatform: {p}")
    print("p-value:", pval)
    print("Median voting:", med_v)
    print("Median non-voting:", med_nv)
    print("Median shift:", med_v - med_nv)
