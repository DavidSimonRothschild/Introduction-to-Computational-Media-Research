#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bar chart of Instagram posts per party using matplotlib with ggplot style
AI GENERATED with claude sonnet 4.5
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Use ggplot style
plt.style.use('ggplot')

# Directory containing Instagram cleaned CSV files
DATA_DIR = "/Users/davidrothschild/Downloads/group work/Introduction-to-Computational-Media-Research/A_Data/2_Instagram/2_CLEAN"

# Load and count posts per party
csv_files = sorted(Path(DATA_DIR).glob("*_cleaned.csv"))

party_counts = []
for csv_file in csv_files:
    # Extract party name from filename
    party_name = csv_file.stem.split('__')[0]
    
    # Read CSV and count rows
    df = pd.read_csv(csv_file)
    count = len(df)
    
    party_counts.append({'Party': party_name, 'Posts': count})

# Create DataFrame
df = pd.DataFrame(party_counts)

# Clean party names for better display
df['Party_Clean'] = df['Party'].str.replace(r'^\d+_', '', regex=True)

# Sort by Posts in descending order
df_sorted = df.sort_values('Posts', ascending=False)

# Create the bar chart
fig, ax = plt.subplots(figsize=(12, 6))

# Create bars with colors
bars = ax.bar(df_sorted['Party_Clean'], df_sorted['Posts'], 
              color=plt.cm.Set3(range(len(df_sorted))))

# Add value labels on top of bars
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 1,
            f'{int(height)}',
            ha='center', va='bottom', fontsize=10, fontweight='bold')

# Customize the plot
ax.set_title('Number of Instagram Posts by Party', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Party', fontsize=13, fontweight='bold')
ax.set_ylabel('Number of Posts', fontsize=13, fontweight='bold')
ax.tick_params(axis='x', rotation=45, labelsize=11)
ax.tick_params(axis='y', labelsize=11)

# Remove top and right spines for cleaner look
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()

# Save the plot as JPG
output_path = '/Users/davidrothschild/Downloads/group work/Introduction-to-Computational-Media-Research/A_Data/Table 1/party_histogram_instagram.jpg'
plt.savefig(output_path, format='jpg', dpi=300, bbox_inches='tight')

print(f"✓ Bar chart saved to: {output_path}")
print("\nParty Post Counts:")
print(df[['Party', 'Posts']].to_string(index=False))
print(f"\nTotal Posts: {df['Posts'].sum()}")

# Display the plot
plt.show()
