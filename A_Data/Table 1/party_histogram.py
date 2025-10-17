#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Histogram of TikTok videos per party using plotnine
AI GENERATED with claude sonnet 4.5
"""

import pandas as pd
from plotnine import *
import warnings
warnings.filterwarnings('ignore')

# Party data
party_data = {
    'Party': ['1_SVP', '2_SP', '3_FDP', '5_Gruene', '7_EVP', '8_JSVP', 
              '9_JUSO', '10_JF', '11_Junge_Mitte', '12_Junge_Gruene', '13_Junge_GLP'],
    'Videos': [102, 62, 32, 55, 32, 17, 25, 26, 15, 14, 9]
}

df = pd.DataFrame(party_data)

# Clean party names for better display
df['Party_Clean'] = df['Party'].str.replace(r'^\d+_', '', regex=True)

# Create the histogram/bar chart
plot = (
    ggplot(df, aes(x='reorder(Party_Clean, -Videos)', y='Videos', fill='Party_Clean')) +
    geom_col(show_legend=False) +
    geom_text(aes(label='Videos'), va='bottom', size=10, nudge_y=2) +
    labs(
        title='Number of TikTok Videos by Party',
        x='Party',
        y='Number of Videos'
    ) +
    theme_minimal() +
    theme(
        figure_size=(12, 6),
        plot_title=element_text(size=16, weight='bold', ha='center'),
        axis_text_x=element_text(rotation=45, ha='right', size=11),
        axis_text_y=element_text(size=11),
        axis_title=element_text(size=13, weight='bold'),
        panel_grid_major_x=element_blank()
    ) +
    scale_fill_brewer(type='qual', palette='Set3')
)

# Save the plot as PDF
output_path = '/Users/davidrothschild/Downloads/group work/Introduction-to-Computational-Media-Research/A_Data/Table 1/party_histogram.pdf'
plot.save(output_path, width=12, height=6)

print(f"✓ Histogram saved to: {output_path}")
print("\nParty Video Counts:")
print(df[['Party', 'Videos']].to_string(index=False))
print(f"\nTotal Videos: {df['Videos'].sum()}")

# Display the plot
print("\nDisplaying plot...")
print(plot)
