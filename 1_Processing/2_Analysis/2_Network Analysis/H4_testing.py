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

NETWORK_INSTAGRAM = PROJECT_ROOT / "1_Processing" / "2_Analysis"/ "2_Network Analysis" / "party_mentions_edges_instagram.csv"
NETWORK_TIKTOK = PROJECT_ROOT / "1_Processing" / "2_Analysis"/ "2_Network Analysis" / "party_mentions_edges_tiktok.csv"

# IMPORTANT: fill / adjust these to your party set (scale is arbitrary, distance uses abs diff)
# source: https://smartmonitor.ch/de/issues/9
IDEOLOGY = {
    # Left
    "JUSO": 4.4,
    "SP": 4.4,

    # Greens
    "Junge Grüne": 5.6,
    "Grüne": 5.6,

    # Christian-social centre-left
    "EVP": 30.9,
    "Junge EVP": 30.9,

    # Green-Liberals
    "Junge GLP": 53.8,
    "GLP": 53.8,

    # Centre
    "Junge Mitte": 62.4,
    "Mitte": 62.4,

    # Liberals
    "JF": 79.8,
    "FDP": 79.8,

    # National-conservatives
    "JSVP": 91.9,
    "SVP": 91.9
}

# ---------- LOAD EDGES ----------

ig = pd.read_csv(NETWORK_INSTAGRAM)
tt = pd.read_csv(NETWORK_TIKTOK)

ig["platform"] = "instagram"
tt["platform"] = "tiktok"

edges = pd.concat([ig, tt], ignore_index=True)


# ---------- IDEOLOGICAL DISTANCE ----------

edges["ideo_dist"] = edges.apply(
    lambda r: abs(IDEOLOGY[r.source_party] - IDEOLOGY[r.target_party]),
    axis=1
)


# ---------- DESCRIPTIVES ----------

print("\n--- Edge descriptives ---")
print(edges[["platform","ideo_dist","mean_engagement","weight"]].describe())


# ---------- H3′ TEST 1: OVERALL SPEARMAN ----------

rho, pval = spearmanr(
    edges["ideo_dist"],
    edges["mean_engagement"],
    alternative="greater"
)

print("\n--- Overall ideological distance vs engagement ---")
print("Spearman rho:", rho)
print("p-value:", pval)


# ---------- H3′ TEST 2: BY PLATFORM ----------

for p in ["instagram","tiktok"]:
    sub = edges[edges.platform == p]
    rho, pval = spearmanr(
        sub["ideo_dist"],
        sub["mean_engagement"],
        alternative="greater"
    )
    print(f"\n{p.upper()} – Spearman rho:", rho, "p-value:", pval)


# ---------- H3′ TEST 3: WEIGHTED REGRESSION ----------

edges["log_weight"] = np.log1p(edges["weight"])

model = smf.wls(
    "mean_engagement ~ ideo_dist * C(platform) + mean_sentiment",
    data=edges,
    weights=edges["weight"]
).fit(cov_type="HC3")

print("\n--- Weighted regression ---")
print(model.summary())