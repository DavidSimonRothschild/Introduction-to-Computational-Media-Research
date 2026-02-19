# Introduction to Computational Media Research – Group Project

Analysis of Swiss political party social media activity on TikTok and Instagram during the 2025 campaign period (March–October 2025). Data was collected via [Zeeschuimer](https://github.com/digitalmethodsinitiative/zeeschuimer) and processed with Python.

---

## Project Structure

```
.
├── A_Data/
│   ├── 1_Tiktok/
│   │   ├── 1_RAW/          # Raw NDJSON exports from Zeeschuimer (TikTok)
│   │   └── 2_CLEAN/        # Cleaned CSV files per party
│   ├── 2_Instagram/
│   │   ├── 1_RAW/          # Raw NDJSON exports from Zeeschuimer (Instagram)
│   │   └── 2_CLEAN/        # Cleaned CSV files per party
│   ├── Table 1/            # Summary tables
│   └── partei_tabelle.csv  # Party reference table
├── 1_Processing/
│   ├── 1_Data_cleaning/
│   │   ├── datacleaner_tiktok.py              # Cleans TikTok NDJSON → CSV
│   │   ├── datacleaner_instagram.py           # Cleans Instagram NDJSON → CSV
│   │   ├── describe_cleaned_Data_Tiktok.py    # Bar chart: posts per party (TikTok)
│   │   └── describe_cleaned_Data_Instagram.py # Bar chart: posts per party (Instagram)
│   └── 2_Analysis/
│       └── 1_Caption_Sentiment/
│           ├── caption_sentiment_analysis.py  # ML-based sentiment (germansentiment)
│           └── sentiment_analysis.py          # Rule-based German sentiment (SentiWS)
├── Synthetic Data/         # Synthetic test data
├── requirements.txt
└── README.md
```

---

## Parties Covered

| # | Party | Platform(s) |
|---|-------|-------------|
| 1 | SVP | TikTok, Instagram |
| 2 | SP | TikTok, Instagram |
| 3 | FDP | TikTok, Instagram |
| 4 | Die Mitte | Instagram |
| 5 | Grüne | TikTok, Instagram |
| 6 | GLP | Instagram |
| 7 | EVP | TikTok, Instagram |
| 8 | JSVP | TikTok, Instagram |
| 9 | JUSO | TikTok, Instagram |
| 10 | Junge Freiheitliche (JF) | TikTok, Instagram |
| 11 | Junge Mitte | TikTok, Instagram |
| 12 | Junge Grüne | TikTok, Instagram |
| 13 | Junge GLP | TikTok, Instagram |
| 14 | Junge EVP | Instagram |

**Data collection period:** 2025-03-09 – 2025-10-12

---

## Setup

**Requirements:** Python 3.9+

```bash
# 1. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt
```

---

## Usage

All scripts use `Path(__file__).resolve()` to locate the project root automatically — no path configuration needed.

### 1. Data Cleaning

```bash
# Clean TikTok raw data → A_Data/1_Tiktok/2_CLEAN/
python 1_Processing/1_Data_cleaning/datacleaner_tiktok.py

# Clean Instagram raw data → A_Data/2_Instagram/2_CLEAN/
python 1_Processing/1_Data_cleaning/datacleaner_instagram.py
```

### 2. Descriptive Statistics

```bash
# Bar chart: total posts per party on TikTok
python 1_Processing/1_Data_cleaning/describe_cleaned_Data_Tiktok.py

# Bar chart: total posts per party on Instagram
python 1_Processing/1_Data_cleaning/describe_cleaned_Data_Instagram.py
```

### 3. Sentiment Analysis

```bash
# ML-based sentiment (germansentiment transformer model) – runs on Instagram SVP data
python 1_Processing/2_Analysis/1_Caption_Sentiment/caption_sentiment_analysis.py

# Rule-based German sentiment (SentiWS) – import and call main("<text>")
python 1_Processing/2_Analysis/1_Caption_Sentiment/sentiment_analysis.py
```

> **Note:** `sentiment_analysis.py` requires SentiWS dictionary files and stopword/negation lists placed in a `data/` folder next to the script (`1_Processing/2_Analysis/1_Caption_Sentiment/data/`).

---

## Dependencies

| Package | Purpose |
|---------|---------|
| `pandas` | Data manipulation |
| `ndjson` | Parsing Zeeschuimer NDJSON exports |
| `matplotlib` | Plotting |
| `germansentiment` | Transformer-based German sentiment model |
| `nltk` | Tokenization (rule-based sentiment) |
