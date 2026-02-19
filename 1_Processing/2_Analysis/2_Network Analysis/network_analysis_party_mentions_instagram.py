from pathlib import Path
import pandas as pd
import os
import re
from collections import Counter

# --- paths ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
input_csv = PROJECT_ROOT / "A_Data" / "2_Instagram" / "2_CLEAN"
output_csv = PROJECT_ROOT / "1_Processing" / "2_Analysis" / "2_Network Analysis"
output_csv.mkdir(parents=True, exist_ok=True)

# --- parties & aliases ---

# Canonical party labels
parties = ["SP", "Grüne", "Mitte", "EVP", "FDP", "GLP", "JF", "SVP"]

# 1) Map from file *stem* (without .csv) to the source party
#    ⚠️ ADJUST THIS to your filenames!
file_to_party = {
    "2_SP__cleaned": "SP",
    "5_Gruene__cleaned": "Grüne",
    "4_Die_Mitte__cleaned": "Mitte",
    "7_EVP__cleaned": "EVP",
    "3_FDP__cleaned": "FDP",
    "6_GLP__cleaned": "GLP",
    "1_SVP__cleaned": "SVP",
    "8_JSVP__cleaned": "JSVP",
    "9_JUSO__cleaned": "JUSO",
    "10_JF__cleaned": "JF",
    "11_Junge_Mitte__cleaned": "Junge Mitte",
    "12_Junge_Gruene__cleaned": "Junge Grüne",
    "13_Junge_GLP__cleaned": "Junge GLP",
    "14_Junge_EVP__cleaned": "Junge EVP",
    # ...
}

# 2) Aliases / spellings for each party as they might appear in captions
#    ⚠️ ADJUST/extend as needed (hashtags, spellings, etc.)
party_aliases = {
    # Mutterparteien
    "SP": [
        "SP",
        "#SP",
        "SP Schweiz",
        "Sozialdemokratische Partei",
        "Sozialdemokraten",
        "Sozialdemokrat:innen",
        "Sozialdemokratische Partei der Schweiz",
        "#spschweiz",
    ],
    "Grüne": [
        "Grüne",
        "Gruene",
        "die Grünen",
        "die Gruenen",
        "Grüne Schweiz",
        "Gruene Schweiz",
        "Grüne Partei",
        "Grünen",
        "Gruenen",
        "#grüne",
        "#gruene",
        "#gruenech",
    ],
    "Mitte": [
        "Mitte",
        "Die Mitte",
        "Die Mitte Schweiz",
        "#DieMitte",
        "#dMitte",
        "Mitte Schweiz",
    ],
    "EVP": [
        "EVP",
        "EVP Schweiz",
        "Evangelische Volkspartei",
        "Evangelische Volkspartei der Schweiz",
        "#EVP",
        "#evpch",
    ],
    "FDP": [
        "FDP",
        "FDP Schweiz",
        "FDP.Die Liberalen",
        "FDP Die Liberalen",
        "FDP – Die Liberalen",
        "Die Liberalen",
        "#FDP",
        "#fdpch",
    ],
    "GLP": [
        "GLP",
        "GLP Schweiz",
        "Grünliberale",
        "Grünliberale Partei",
        "Grünliberale Schweiz",
        "#GLP",
        "#glpch",
    ],
    "SVP": [
        "SVP",
        "SVP Schweiz",
        "Schweizerische Volkspartei",
        "Volkspartei",
        "#SVP",
        "#svpch",
    ],

    # Jungparteien / Nachwuchs
    "JSVP": [
        "JSVP",
        "Junge SVP",
        "Jung-SVP",
        "Junge SVP Schweiz",
        "#JSVP",
        "#jungesvp",
        "#jsvpch",
    ],
    "JUSO": [
        "JUSO",
        "Juso",
        "JUSO Schweiz",
        "Juso Schweiz",
        "Jungsozialist:innen",
        "Jungsozialisten",
        "#JUSO",
        "#juso",
        "#jusoCH",
    ],
    "JF": [
        "JF",
        "Jungfreisinn",
        "Jungfreisinnige",
        "Jungfreisinnige Schweiz",
        "Jungfreisinnige Partei",
        "#JF",
        "#jungfreisinn",
        "#jungfreisinnige",
    ],
    "Junge Mitte": [
        "Junge Mitte",
        "Junge Mitte Schweiz",
        "Jungemitte",
        "Jung-Mitte",
        "#jungemitte",
        "#jungemitteCH",
    ],
    "Junge Grüne": [
        "Junge Grüne",
        "Junge Gruene",
        "Junggrüne",
        "Junggruene",
        "Junge Grüne Schweiz",
        "Junggrüne Schweiz",
        "#jungegrüne",
        "#junggrüne",
        "#junggruene",
    ],
    "Junge GLP": [
        "Junge GLP",
        "Jung-GLP",
        "JungGLP",
        "Junggrünliberale",
        "Junggrünliberale Schweiz",
        "#jungeglp",
        "#jungglp",
    ],
    "Junge EVP": [
        "Junge EVP",
        "Jung-EVP",
        "JungEVP",
        "Junge EVP Schweiz",
        "#jungeevp",
        "#jungevp",
    ],
}


# Compile regex patterns for mentions (case-insensitive, try to respect word boundaries)
party_patterns = {
    party: re.compile(
        r"(?<!\w)(" + "|".join(map(re.escape, aliases)) + r")(?!\w)",
        flags=re.IGNORECASE
    )
    for party, aliases in party_aliases.items()
}

# --- count edges (source_party, target_party) ---
edges = Counter()

for filename in os.listdir(input_csv):
    if not filename.endswith(".csv"):
        continue

    filepath = input_csv / filename
    file_stem = Path(filename).stem  # e.g. "spschweiz"

    source_party = file_to_party.get(file_stem)
    if source_party is None:
        print(f"⚠️ No party mapping for file {filename}, skipping.")
        continue

    df = pd.read_csv(filepath)

    if "data.caption.text" not in df.columns:
        print(f"⚠️ No 'data.caption.text' column in {filename}, skipping.")
        continue

    for text in df["data.caption.text"].dropna().astype(str):
        mentioned_targets = set()

        for target_party, pattern in party_patterns.items():
            if target_party == source_party:
                continue  # ignore self-mentions if you don't want loops

            if pattern.search(text):
                mentioned_targets.add(target_party)

        # Each post counts at most once per (source → target) pair
        for target_party in mentioned_targets:
            edges[(source_party, target_party)] += 1

# --- build edge table ---
edges_df = pd.DataFrame(
    [
        {"source_party": s, "target_party": t, "weight": w}
        for (s, t), w in edges.items()
    ]
)

# save for network analysis
edges_df.to_csv(output_csv / "party_mentions_edges_instagram.csv", index=False)
print(edges_df)
