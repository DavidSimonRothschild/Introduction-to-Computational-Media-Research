#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bar chart of TikTok videos per party using matplotlib with ggplot style
AI GENERATED with claude sonnet 4.5
"""

import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# Use ggplot style
plt.style.use('ggplot')

# Party data
party_data = {
    'Party': ['1_SVP', '2_SP', '3_FDP', '5_Gruene', '7_EVP', '8_JSVP', 
              '9_JUSO', '10_JF', '11_Junge_Mitte', '12_Junge_Gruene', '13_Junge_GLP'],
    'Videos': [102, 62, 32, 55, 32, 17, 25, 26, 15, 14, 9]
}

df = pd.DataFrame(party_data)

# Clean party names for better display
df['Party_Clean'] = df['Party'].str.replace(r'^\d+_', '', regex=True)

# Sort by Videos in descending order
df_sorted = df.sort_values('Videos', ascending=False)

# Create the bar chart
fig, ax = plt.subplots(figsize=(12, 6))

# Create bars with colors
bars = ax.bar(df_sorted['Party_Clean'], df_sorted['Videos'], 
              color=plt.cm.Set3(range(len(df_sorted))))

# Add value labels on top of bars
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 1,
            f'{int(height)}',
            ha='center', va='bottom', fontsize=10, fontweight='bold')

# Customize the plot
ax.set_title('Number of TikTok Videos by Party', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Party', fontsize=13, fontweight='bold')
ax.set_ylabel('Number of Videos', fontsize=13, fontweight='bold')
ax.tick_params(axis='x', rotation=45, labelsize=11)
ax.tick_params(axis='y', labelsize=11)

# Remove top and right spines for cleaner look
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()

# Save the plot as PDF
output_path = '/Users/davidrothschild/Downloads/group work/Introduction-to-Computational-Media-Research/A_Data/Table 1/party_histogram.pdf'
plt.savefig(output_path, format='pdf', dpi=300, bbox_inches='tight')

print(f"✓ Bar chart saved to: {output_path}")
print("\nParty Video Counts:")
print(df[['Party', 'Videos']].to_string(index=False))
print(f"\nTotal Videos: {df['Videos'].sum()}")

# Display the plot
plt.show()
