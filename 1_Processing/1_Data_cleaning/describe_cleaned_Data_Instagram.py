# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ---- CONFIG ----
INPUT_DIR = Path("/Users/nickeichmann/PythonProjects/Introduction-to-Computational-Media-Research/A_Data/2_Instagram/2_CLEAN")
SAVE_PNG   = True  # set to False if you only want to plt.show()
OUTPUT_PNG = INPUT_DIR / "Instagram_total_posts_per_party_colored.png"
# ----------------

# Swiss party color keywords -> hex (add/adjust as needed)
PARTY_COLOR_MAP = {
    # keyword(s)       # color
    "svp":            "#7AC143",  # SVP/UDC green
    "udc":            "#7AC143",
    "sp":             "#E3001B",  # SP/PS red
    "ps":             "#E3001B",
    "fdp":            "#0F5AA6",  # FDP/PLR blue
    "plr":            "#0F5AA6",
    "mitte":          "#F28E00",  # Die Mitte / Le Centre orange
    "centre":         "#F28E00",
    "glp":            "#B7CF00",  # GLP lime
    "pvl":            "#B7CF00",
    "gps":            "#3AAA35",  # GPS / Grüne / Les Verts green
    "grüne":          "#3AAA35",
    "gruene":         "#3AAA35",
    "verts":          "#3AAA35",
    "evp":            "#FFD400",  # EVP yellow
    "edu":            "#00529B",  # EDU blue
    "lega":           "#6C757D",  # Lega grey
    "pda":            "#B30000",  # PdA dark red
    "al":             "#8E44AD",  # Alternative Liste purple
}

DEFAULT_COLOR = "#6E8093"  # fallback if no keyword matches

def color_for_party(party_name: str) -> str:
    """Return a party color based on keywords in the party name."""
    if not isinstance(party_name, str):
        return DEFAULT_COLOR
    name = party_name.lower()
    for kw, col in PARTY_COLOR_MAP.items():
        if kw in name:
            return col
    return DEFAULT_COLOR

# ---- Load all CSVs and add a 'party' column from the filename ----
files = sorted(p for p in INPUT_DIR.iterdir() if p.is_file() and p.suffix.lower() == ".csv")
if not files:
    raise FileNotFoundError(f"No CSV files found in {INPUT_DIR}")

dfs = []
for fp in files:
    df_i = pd.read_csv(fp)
    party = fp.stem[:-8] if fp.stem.endswith("_cleaned") else fp.stem
    df_i["party"] = party
    dfs.append(df_i)

df = pd.concat(dfs, ignore_index=True)

# ---- Total posts per party ----
counts = (
    df["party"]
    .astype("string")
    .value_counts()
    .sort_values(ascending=False)
)

# Colors per bar
bar_colors = [color_for_party(p) for p in counts.index.tolist()]

# ---- Plot ----
plt.figure(figsize=(10, 5))
bars = plt.bar(range(len(counts)), counts.values, color=bar_colors)

plt.xticks(range(len(counts)), counts.index, rotation=30, ha="right")
plt.title("Total TikTok Posts per Party")
plt.xlabel("Party")
plt.ylabel("Total Posts")

# Add value labels on top of bars
for rect, val in zip(bars, counts.values):
    height = rect.get_height()
    plt.text(
        rect.get_x() + rect.get_width() / 2.0,
        height,
        f"{int(val)}",
        ha="center",
        va="bottom",
        fontsize=10
    )

plt.tight_layout()

if SAVE_PNG:
    plt.savefig(OUTPUT_PNG, dpi=150)
else:
    plt.show()
