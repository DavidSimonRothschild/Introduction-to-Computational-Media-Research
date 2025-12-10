# How Swiss Parties Mobilize Voters on Instagram and TikTok

### ICMR Fall semester 2025

**Group**: Nick Eichmann, Marc Eggenberger, Sarah Häusermann, David Rothschild

**Date of submission**: January 5, 2025

## 1: Introduction

In Switzerland, not every vote captures public attention. While a handful of nationwide decisions dominate headlines and ignite political debate, many others unfold quietly in the background. Political actors still take significant energy to shaping how these issues are perceived. Increasingly, they do so on platforms that were not built for politics at all.

Instagram and TikTok have become central arenas where Swiss parties attempt to mobilize younger audiences, experiment with new communication styles, and compete for visibility.

Unlike traditional campaign periods, communication around these votes does not follow a neatly defined electoral cycle. Instead, it unfolds as a continuous timeline, shaped by platform dynamics: fluctuating posting frequencies, strategic content closer to voting dates, and the use of emotional messaging to capture attention.

## 2: Method

### 2.1: Engagement-Score

#### 2.1.1: Instagram Engagement Score (mean-centered)

The engagement score measures how strongly an Instagram post performs compared to the *average post of the same party*.

For each post `i`, we first compute a raw engagement score:

`raw_engagement_i = (likes_i / avg_likes)
                   + (comments_i / avg_comments)`

Both averages (`avg_likes`, `avg_comments`) are calculated **within the same CSV (party)**.

We then mean-center the score within each CSV:

`engagement_score_i = raw_engagement_i - mean(raw_engagement)`

**Interpretation:**

- `0`   → average post  
- `> 0` → above-average engagement  
- `< 0` → below-average engagement

#### 2.1.2: TikTok Engagement Score (mean-centered)

The engagement score measures how strongly a TikTok video performs compared to the *average video of the same party*.

For each video `i`, we first compute a raw engagement score:

`raw_engagement_i = (likes_i / avg_likes)
                   + (comments_i / avg_comments)
                   + (shares_i / avg_shares)
                   + (views_i / avg_views)`

All averages (`avg_likes`, `avg_comments`, `avg_shares`, `avg_views`) are calculated **within the same CSV (party)**.

We then mean-center the score within each CSV:

`engagement_score_i = raw_engagement_i - mean(raw_engagement)`

**Interpretation:**

- `0`   → average video  
- `> 0` → above-average engagement  
- `< 0` → below-average engagement
