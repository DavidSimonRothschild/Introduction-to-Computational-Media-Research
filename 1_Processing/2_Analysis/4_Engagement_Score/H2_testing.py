import pandas as pd
import glob
import os
from pathlib import Path
import numpy as np
from scipy.stats import spearmanr
import statsmodels.formula.api as smf


# ---------------- CONFIG ----------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
INSTAGRAM_FOLDER = PROJECT_ROOT / "A_Data" / "2_Instagram" / "2_CLEAN"
TIKTOK_FOLDER = PROJECT_ROOT / "A_Data" / "1_Tiktok" / "2_CLEAN"

VOTING_DAY = pd.Timestamp("2025-09-28")


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
df = df.dropna(subset=["engagement_score", "voting.topic", "data.createTime"])


# ---------------- TIME TO VOTE ----------------

df["post_date"] = pd.to_datetime(df["data.createTime"])
df["days_to_vote"] = (VOTING_DAY - df["post_date"]).dt.days

# keep only pre-vote period
pre_vote = df[df["days_to_vote"] >= 0]


# ---------------- H2: SPEARMAN TEST ----------------

rho, pval = spearmanr(
    pre_vote["days_to_vote"],
    pre_vote["engagement_score"],
    alternative="less"
)

print("\n--- H2: Distance to voting date vs engagement (pre-vote only) ---")
print("Spearman rho:", rho)
print("p-value:", pval)


# ---------------- BINNED MEDIANS ----------------

pre_vote["time_bin"] = pd.cut(
    pre_vote["days_to_vote"],
    bins=[0,7,30,90,180],
    labels=["0-7d","8-30d","31-90d","91-180d"]
)

print("\n--- Median engagement by time bin (pre-vote) ---")
print(pre_vote.groupby("time_bin")["engagement_score"].median())


