# Colab Instructions - Reproducing All Analyses

## Quick Start

**Main Analysis Notebook (Hypothesis Tests):**
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/DavidSimonRothschild/Introduction-to-Computational-Media-Research/blob/main/analysis_notebook.ipynb)

This notebook contains all four hypothesis tests (H1-H4) and loads pre-computed data.

---

## What's Included

The Colab notebook automatically:
1. Clones this repository
2. Loads all data from `A_Data/`
3. Runs statistical tests for all four hypotheses

### Data Already Computed

All analysis results are **pre-computed** and stored in the CSV files in `A_Data/`:

- **Sentiment scores** (`sentiment_rulebased` column) - computed by `1_Processing/2_Analysis/1_Caption_Sentiment/`
- **Voting topic labels** (`voting.topic` column) - computed by `1_Processing/2_Analysis/3_Label_Posts_Voting_Topic/`
- **Engagement scores** (`engagement_score` column) - computed by `1_Processing/2_Analysis/4_Engagement_Score/`
- **Network edges** - computed by `1_Processing/2_Analysis/2_Network Analysis/`

### What the Notebook Does

The notebook performs the **statistical tests** on the pre-computed data:

- **H1**: Mann-Whitney U test (voting vs non-voting engagement)
- **H2**: Spearman correlation (temporal proximity to vote)
- **H3**: OLS regression (sentiment vs engagement)
- **H4**: Spearman correlation (ideological distance vs engagement)

---

## Running Original Analysis Scripts

If you want to re-run the **original data processing scripts** (sentiment analysis, labeling, etc.), you can do so in Colab:

### 1. Clone the Repository

```python
!git clone https://github.com/DavidSimonRothschild/Introduction-to-Computational-Media-Research.git
%cd Introduction-to-Computational-Media-Research
```

### 2. Install Dependencies

```python
!pip install pandas nltk
```

### 3. Run Individual Scripts

#### Sentiment Analysis (TikTok)
```python
!python 1_Processing/2_Analysis/1_Caption_Sentiment/sentiment_analysis_tiktok.py
```

#### Sentiment Analysis (Instagram)
```python
!python 1_Processing/2_Analysis/1_Caption_Sentiment/sentiment_analysis_instagram.py
```

#### Label Voting Topics
```python
!python 1_Processing/2_Analysis/3_Label_Posts_Voting_Topic/label_posts.py
```

#### Engagement Score (Instagram)
```python
!python 1_Processing/2_Analysis/4_Engagement_Score/1_Engagement_score_Instagram.py
```

#### Engagement Score (TikTok)
```python
!python 1_Processing/2_Analysis/4_Engagement_Score/2_Engagement_score_Tiktok.py
```

#### Network Analysis (Instagram)
```python
!python 1_Processing/2_Analysis/2_Network\ Analysis/network_analysis_party_mentions_instagram.py
```

#### Network Analysis (TikTok)
```python
!python 1_Processing/2_Analysis/2_Network\ Analysis/network_analysis_party_mentions_tiktok.py
```

---

## Folder Structure

```
1_Processing/2_Analysis/
├── 1_Caption_Sentiment/       # Sentiment analysis scripts + lexicons
├── 2_Network Analysis/         # Party mention network analysis
├── 3_Label_Posts_Voting_Topic/ # Voting topic labeling
└── 4_Engagement_Score/         # Engagement score calculation
```

All scripts read from `A_Data/` and write results back to the same CSV files.

---

## Notes

- The main notebook (`analysis_notebook.ipynb`) is **ready to run** and contains all hypothesis tests
- Original processing scripts are available in `1_Processing/2_Analysis/` if you want to re-compute the data
- All data and scripts are in the GitHub repository and accessible via Colab
