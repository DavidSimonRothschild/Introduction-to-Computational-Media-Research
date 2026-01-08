# How Swiss Parties Mobilize Voters on Instagram and TikTok

*Link to Colab Notebook:*

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/DavidSimonRothschild/Introduction-to-Computational-Media-Research/blob/main/analysis_notebook.ipynb)

**Course**: Introduction to Computational Media Research (ICMR)  
**Institution**: University of Zurich (UZH), Department of Communication and Media Research  
**Semester**: Fall 2025

**Contributors**: Nick Eichmann, Marc Eggenberger, Sarah Häusermann, David Rothschild

## Overview

This repository contains the code and data for our research paper analyzing how Swiss political parties use Instagram and TikTok to mobilize voters. We test four hypotheses about engagement drivers:

- **H1**: Voting-related posts generate higher engagement
- **H2**: Posts closer to voting day generate higher engagement  
- **H3**: Negative sentiment drives higher engagement
- **H4**: Cross-party interactions with ideologically distant parties generate higher engagement

## Reproducibility

**Click the "Open in Colab" badge above** to run all analyses in Google Colab without any local setup.

The notebook will:
1. Clone this repository
2. Install dependencies
3. Run all four hypothesis tests
4. Display results

## Repository Structure

```
├── analysis_notebook.ipynb    # Main reproducible notebook (Colab-ready)
├── 1_Processing/              # Data processing and analysis scripts
│   ├── 1_Data_cleaning/       # Data cleaning scripts
│   └── 2_Analysis/            # Hypothesis testing scripts
│       ├── 1_Caption_Sentiment/
│       ├── 2_Network Analysis/
│       ├── 3_Label_Posts_Voting_Topic/
│       └── 4_Engagement_Score/
├── 2_Paper/                   # Paper manuscript
├── A_Data/                    # Data files
│   ├── 1_Tiktok/
│   └── 2_Instagram/
└── requirements.txt           # Python dependencies
```

## Local Setup

```bash
git clone https://github.com/DavidSimonRothschild/Introduction-to-Computational-Media-Research.git
cd Introduction-to-Computational-Media-Research
pip install -r requirements.txt
jupyter notebook analysis_notebook.ipynb
```

## Results Summary

| Hypothesis | Result |
|------------|--------|
| H1: Voting → Engagement | ❌ Rejected (opposite effect) |
| H2: Proximity → Engagement | ❌ Rejected |
| H3: Negativity → Engagement | ❌ Rejected |
| H4: Ideological Distance → Engagement | ❌ Rejected |
