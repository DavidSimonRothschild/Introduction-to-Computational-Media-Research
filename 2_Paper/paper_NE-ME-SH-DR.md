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

## 2.2: Sentiment Analysis
To quantify the sentiment of party posts, we applied the rule-based framework Germotion, which is specifically designed for the German language. Germotion tokenizes captions using a pretrained German sentence tokenizer combined with the Treebank word tokenizer, removes punctuation and stopwords, and matches all remaining tokens against two sentiment lexicons derived from the German SentiWS dictionary. These lexicons assign continuous polarity scores in the interval from −1 to +1 to both positive and negative word forms, including their inflected variants.

The algorithm additionally implements a simple negation-handling mechanism: if a sentiment-bearing token is preceded or followed by a negation term such as nicht, nie, or kein, the corresponding sentiment contribution is inverted and downweighted by 50 percent. Sentiment values are aggregated across all detected tokens within a post, and the resulting score is clipped to the interval [−1, 1]. This transparent, dictionary-based procedure ensures that sentiment scores are directly interpretable and well suited for the analysis of German-language political communication.

Github: https://github.com/pascalhuszar/Germotion

# 3 Results

## 3.1: H1: Posts connecting to the latest voting issues get higher engagement than posts related to non-voting issues
### 3.1.1: Method

To test whether posts that reference current voting issues receive higher engagement than non-voting posts (H1), we combine post-level data from the official Instagram and TikTok accounts of Swiss political parties and their youth organisations. The dataset consists of all posts published between 9 March and 12 October 2025. For each post we observe a composite engagement score capturing user reactions such as likes, comments, and shares (explained i the previous section).


Posts were classified as voting-related using a keyword-based labelling procedure applied to the textual content of captions on Instagram and descriptions on TikTok. We defined two topical dictionaries corresponding to the two national ballots held during the observation period: the electronic identity initiative (E-ID) and the Eigenmietwert reform. Each post was assigned a categorical label taking the value zero if no voting-related keywords were present, one if only electronic identity terms were detected, two if only Eigenmietwert-related terms were detected, and three if terms from both dictionaries were present. For the main hypothesis test, this variable is collapsed into a binary indicator that equals one if the post references at least one voting topic and zero otherwise.

#### 3.1.2: Hypothesis Test

Let Yi denote the engagement score of post i. Hypothesis H1 states that the expected engagement of voting-related posts is greater than the expected engagement of non-voting posts. The null hypothesis is that the expected engagement of voting-related posts is less than or equal to the expected engagement of non-voting posts.

Because the engagement distribution is highly skewed and contains extreme values, we employ a one-sided Mann–Whitney U test to compare the distribution of engagement scores between voting-related and non-voting posts. This non-parametric procedure does not rely on distributional assumptions and is robust to outliers, making it suitable for social media engagement data.

We conduct the test on the pooled sample as well as separately for Instagram and TikTok to assess whether the relationship between voting-related content and engagement differs across platforms. In addition, we report median engagement differences between the two groups as an interpretable measure of effect size.

Together, this procedure allows us to evaluate whether references to current voting issues are associated with systematically higher engagement levels while accounting for the non-normal nature of the outcome variable.

### 3.1.3: Results
We find strong evidence against Hypothesis H1. Not only do voting-related posts fail to generate higher engagement, but they are associated with significantly lower engagement compared to non-voting posts.

A one-sided Mann–Whitney U test comparing all voting-related posts (n=371) with non-voting posts (n=1420) yields a p-value of 0.97 in the hypothesised direction. Reversing the alternative hypothesis shows that voting-related posts in fact receive significantly lower engagement than non-voting content (p < 0.05). This indicates that the effect is statistically significant in the opposite direction of H1.

Table 1 reports median engagement scores by content type.

| Content type | Median engagement |
|--------------|------------------|
| Voting-related | −1.05 |
| Non-voting | −0.91 |
| Median difference (voting – non-voting) | −0.14 |

The negative median difference confirms that voting-related posts systematically underperform.

The effect of voting-related content differs substantially between platforms. On Instagram, posts referring to current voting issues receive markedly lower engagement than non-voting posts. The median engagement score of voting-related posts is −0.94, compared to −0.79 for non-voting posts, corresponding to a negative median shift of −0.14. This difference is statistically significant in the opposite direction of Hypothesis H1.

On TikTok, in contrast, voting-related posts do not exhibit a systematic engagement penalty. Median engagement for voting-related posts is −2.24, compared to −2.25 for non-voting content, yielding a negligible median shift of +0.02. The difference is statistically insignificant.

| Platform  | Median engagement (voting) | Median engagement (non-voting) | Median shift |
|-----------|----------------------------|---------------------------------|--------------|
| Instagram | −0.94                      | −0.79                           | −0.14        |
| TikTok    | −2.24                      | −2.25                           | +0.02        |

These findings indicate that the overall negative effect of voting-related content is driven almost entirely by Instagram, whereas TikTok shows a largely neutral response pattern.

## 3.2: H2: Posts that are closer to the voting date generate higher user engagement than posts further from voting date
### 3.2.1: Method
To examine whether posts published closer to the voting day receive higher engagement than posts published further in advance (H2), we analyse the temporal dynamics of voting-related content on Instagram and TikTok.

The observation window spans from 9 March to 12 October 2025. Both voting issues under study were decided in a national ballot on 28 September 2025. For each post, the publication date is extracted from the platform metadata and converted into a calendar date.

We compute the number of days between the publication date of each post and the voting day on 28 September 2025. This variable takes positive values for posts published before the vote, zero for posts published on the voting day, and negative values for posts published after the ballot. To ensure that the analysis captures mobilisation dynamics rather than post-election communication, we restrict the sample to posts published on or before the voting day.

#### 3.2.2: Hypothesis Test
Let Yi denote the engagement score of post i and let DaysToVote denote the number of days between the publication date and the voting day. Hypothesis H2 states that engagement increases as the voting day approaches, implying that posts with fewer days remaining until the vote receive higher engagement.

Because neither engagement nor the time-to-vote variable follow a normal distribution and because the relationship is expected to be monotonic rather than linear, we employ a one-sided Spearman rank correlation test to assess whether engagement is negatively associated with the number of days remaining until the vote.

To facilitate interpretation, we further group posts into four temporal bins: posts published within 7 days of the vote, between 8 and 30 days, between 31 and 90 days, and between 91 and 180 days before the vote. For each bin, we compute the median engagement score.

## 3.2.3: Results

Hypothesis H2 is not supported by the data. Contrary to expectations, engagement does not increase as the voting day approaches. Instead, posts published further away from the ballot date receive higher engagement.

A one-sided Spearman rank correlation test on all voting-related posts published before the voting day yields a positive correlation between the number of days remaining until the vote and engagement, with a Spearman coefficient of 0.20 and a p-value of 0.999. This indicates that engagement tends to be higher for posts that are published earlier rather than closer to the vote.

The binned median analysis reinforces this finding. Table 3 reports median engagement scores by temporal distance to the voting day.

| Days before vote | Median engagement |
|------------------|------------------|
| 0–7 days         | −2.28 |
| 8–30 days        | −2.77 |
| 31–90 days       | −2.33 |
| 91–180 days      | −1.68 |

Engagement is lowest in the final month prior to the ballot and peaks in the period three to six months before the voting day. This non-monotonic pattern suggests a campaign fatigue effect, whereby audiences disengage from repeated mobilisation attempts as the vote approaches.

In sum, Hypothesis H2 is rejected. Rather than intensifying closer to the voting day, user engagement with voting-related content declines in the final stages of the campaign period.

## 3.3: H3: The higher the negativity score, the higher the engagement of a post

### 3.3.1: Method

To assess whether more negative language is associated with higher user engagement (H3), we analyse the relationship between the sentiment of political posts and their engagement scores.  Each post is assigned a sentiment score using a rule-based sentiment analysis approach applied to the caption text on Instagram and the description text on TikTok. The resulting variable, `sentiment_rulebased`, ranges from negative to positive values, with lower scores indicating more negative tone and higher scores indicating more positive tone.

For each party separately, we estimate an ordinary least squares regression in which the engagement score is regressed on the sentiment score. This allows us to identify whether within-party variation in tone is associated with systematic differences in engagement. To account for heteroscedasticity in engagement outcomes, we use heteroscedasticity-robust standard errors.

In addition to party-level models, we estimate a pooled regression that combines posts from all parties. This pooled specification allows us to test for an overall association between sentiment and engagement across the entire dataset.

### 3.3.2: Hypothesis Test

Hypothesis H3 states that posts with more negative tone receive higher engagement. Because higher values of the sentiment score indicate more positive tone, support for H3 is indicated by a negative regression coefficient on the sentiment variable. That is, an increase in positivity should be associated with lower engagement if negativity indeed drives user interaction.

This procedure enables a systematic evaluation of whether negative emotional framing mobilises users more effectively than positive or neutral language.

## 3.3.3: Results
Hypothesis H3 is not supported by the data. Across platforms, there is no systematic relationship between the sentiment of posts and user engagement.

For Instagram, the pooled regression yields a negative coefficient for the sentiment variable, indicating that more negative tone is weakly associated with higher engagement. However, this effect is small and statistically insignificant (beta = −0.17, p = 0.21, R² = 0.001). Party-level analyses reveal that almost all parties exhibit coefficients close to zero and large standard errors. The only marginal exception is the FDP, for which the coefficient is negative and borderline significant (beta = −0.65, p = 0.055), suggesting that FDP posts with more negative tone may receive slightly higher engagement. This effect, however, does not generalise to other parties.

For TikTok, the pooled regression shows a positive but statistically insignificant association between sentiment and engagement (beta = 0.39, p = 0.55, R² = 0.0004). This indicates that on TikTok, if anything, more positive tone is weakly associated with higher engagement, again contradicting H3. Party-level models on TikTok exhibit large uncertainty and no robust or consistent effects.

Taken together, these findings demonstrate that negativity does not systematically drive engagement in Swiss political social media communication. While there is weak and isolated evidence for a negativity effect among FDP posts on Instagram, this pattern does not extend across parties or platforms. Hypothesis H3 is therefore rejected.

## 3.4: H4: If parties engage with each other, posts have higher engagement, if these parties are ideologically further away from each other 
### 3.4.1: Method

To test whether posts in which parties engage with ideologically distant opponents receive higher engagement (H4), we combine post-level engagement information with an interaction network of party mentions.

We identify cross-party interactions by detecting explicit mentions of other parties in the caption text on Instagram and the description text on TikTok. Using a comprehensive dictionary of party name variants and hashtags, we detect when a post published by a given source party references another target party. Each post contributes at most once to a given source–target pair.

For each platform separately, we aggregate these interactions into an edge-level dataset, where each observation represents a directed interaction from a source party to a target party. For each source–target pair, we compute the number of posts in which the interaction occurs and the mean engagement score of those posts.

The Measurement of Ideological Distance was computed by the Smart vote Left-Right scores (https://smartmonitor.ch/de/issues/9). All parties are positioned on a continuous left–right ideological scale derived from parliamentary voting behaviour. Youth organisations are assigned the ideological score of their parent party. For each source–target pair, ideological distance is defined as the absolute difference between the ideological positions of the source and the target party.

### 3.4.2: Hypothesis Test
Hypothesis H4 states that posts in which parties engage with ideologically more distant opponents receive higher engagement than interactions between ideologically proximate parties.

To test this hypothesis, we compute a one-sided Spearman rank correlation between ideological distance and mean engagement across all source–target party pairs. This non-parametric test assesses whether interactions involving larger ideological distances are associated with systematically higher engagement, without imposing linearity assumptions.

Hypothesis H4 is supported if ideological distance is positively and significantly correlated with mean engagement, indicating that interactions between ideologically distant parties are associated with higher engagement.

### 4.3.3: Results
Figure X visualises the network of cross-party mentions on Instagram. Nodes represent political parties, with node size indicating overall interaction strength and colour reflecting party affiliation. Edges denote directed mentions from a source party to a target party, with arrow thickness proportional to the number of posts in which the interaction occurs.

The network reveals a highly asymmetric interaction structure. Right-wing parties, particularly the SVP and its youth organisation JSVP, occupy a central position with numerous incoming mentions from ideologically diverse parties, whereas left and green parties appear more peripheral and engage less frequently across ideological blocks. Interactions are not evenly distributed along the ideological spectrum but are instead concentrated on a small number of focal actors. This descriptive pattern suggests that a few polarising parties act as attention hubs in cross-party communication, while most parties primarily remain within their ideological neighbourhoods.

![party_mentions_network_instagram.png](../1_Processing/2_Analysis/2_Network%20Analysis/party_mentions_network_instagram.png)

Figure Y visualises the network of cross-party mentions on TikTok. Compared to Instagram, the TikTok network is substantially sparser and more centralised around a small number of actors.

The SVP clearly dominates the interaction structure. It receives a large number of incoming mentions, particularly from its youth organisation JSVP, which forms the strongest dyadic connection in the network. This indicates that TikTok interactions are heavily concentrated within the right-wing ideological block rather than across ideological boundaries.

Cross-ideological interactions are rare and mostly unidirectional. For example, FDP and JUSO occasionally mention ideologically distant parties, but these links are weak and not reciprocated. Left and green parties are largely isolated, with very few outgoing or incoming ties.

![party_mentions_network_tiktok.png](../1_Processing/2_Analysis/2_Network%20Analysis/party_mentions_network_tiktok.png)

Hypothesis H4 is not supported by the data. Across all source–target party interactions, there is no evidence that ideological distance is associated with higher engagement.

Descriptive statistics indicate substantial heterogeneity in both ideological distance and mean engagement across interactions. The average ideological distance is 45.7 points on the left–right scale, with values ranging from zero to 87.5. Mean engagement is highly dispersed, ranging from −3.65 to 32.36.

A one-sided Spearman rank correlation test reveals no monotonic association between ideological distance and mean engagement (rho = 0.01, p = 0.46). Platform-specific analyses yield similarly null results. On Instagram, the correlation is 0.03 (p = 0.42), while on TikTok it is −0.01 (p = 0.53).

Overall, the TikTok network shows a fragmented and polarised communication structure. Engagement is concentrated on a small number of right-wing actors, and genuine cross-ideological interaction is largely absent. This structural pattern is consistent with the null results of the statistical tests and further supports the rejection of Hypothesis H4.
