#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to create Table 1 (Descriptive Statistics) for TikTok data
AI GENERATED with claude sonnet 4.5
"""

import pandas as pd
import os
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np

# Directory containing the cleaned CSV files
DATA_DIR = "/Users/davidrothschild/Downloads/group work/Introduction-to-Computational-Media-Research/A_Data/1_Tiktok/2_CLEAN"
OUTPUT_PDF = "/Users/davidrothschild/Downloads/group work/Introduction-to-Computational-Media-Research/A_Data/Table 1/Table1_TikTok.pdf"

def load_all_data():
    """Load all CSV files and combine them into a single DataFrame"""
    all_data = []
    
    # Get all CSV files in the directory
    csv_files = sorted(Path(DATA_DIR).glob("*_cleaned.csv"))
    
    for csv_file in csv_files:
        # Extract party name from filename
        party_name = csv_file.stem.split('__')[0]
        
        # Read CSV
        df = pd.read_csv(csv_file)
        df['party'] = party_name
        all_data.append(df)
    
    # Combine all data
    combined_df = pd.concat(all_data, ignore_index=True)
    
    # Convert createTime to datetime
    combined_df['data.createTime'] = pd.to_datetime(combined_df['data.createTime'])
    
    return combined_df

def create_descriptive_table(df):
    """Create descriptive statistics table"""
    
    # Columns for statistics
    stat_columns = [
        'data.stats.collectCount',
        'data.stats.commentCount', 
        'data.stats.diggCount',
        'data.stats.playCount',
        'data.stats.shareCount'
    ]
    
    # Create table for overall statistics
    overall_stats = pd.DataFrame()
    
    for col in stat_columns:
        col_clean_name = col.replace('data.stats.', '').replace('Count', '')
        overall_stats.loc[col_clean_name, 'Mean'] = df[col].mean()
        overall_stats.loc[col_clean_name, 'Median'] = df[col].median()
        overall_stats.loc[col_clean_name, 'Std Dev'] = df[col].std()
        overall_stats.loc[col_clean_name, 'Min'] = df[col].min()
        overall_stats.loc[col_clean_name, 'Max'] = df[col].max()
        overall_stats.loc[col_clean_name, 'Total'] = df[col].sum()
    
    # Add general statistics
    general_stats = pd.DataFrame()
    general_stats.loc['Total Videos', 'Value'] = len(df)
    general_stats.loc['Total Parties', 'Value'] = df['party'].nunique()
    general_stats.loc['Date Range Start', 'Value'] = df['data.createTime'].min().strftime('%Y-%m-%d')
    general_stats.loc['Date Range End', 'Value'] = df['data.createTime'].max().strftime('%Y-%m-%d')
    
    # Create party-level statistics
    party_stats = df.groupby('party').agg({
        'data.id': 'count',
        'data.stats.playCount': ['mean', 'sum'],
        'data.stats.diggCount': ['mean', 'sum'],
        'data.stats.commentCount': ['mean', 'sum'],
        'data.stats.shareCount': ['mean', 'sum'],
        'data.stats.collectCount': ['mean', 'sum']
    }).round(2)
    
    party_stats.columns = ['_'.join(col).strip() for col in party_stats.columns.values]
    party_stats = party_stats.rename(columns={'data.id_count': 'Video Count'})
    
    return overall_stats, general_stats, party_stats

def create_pdf_table(overall_stats, general_stats, party_stats, output_path):
    """Create PDF with tables"""
    
    with PdfPages(output_path) as pdf:
        # Page 1: General and Overall Statistics
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 14))
        fig.suptitle('Table 1: Descriptive Statistics - TikTok Data', 
                     fontsize=16, fontweight='bold', y=0.98)
        
        # General Statistics
        ax1.axis('tight')
        ax1.axis('off')
        ax1.set_title('General Statistics', fontsize=14, fontweight='bold', pad=20)
        
        general_data = [[idx, f"{val:.0f}" if isinstance(val, (int, float)) else val] 
                       for idx, val in general_stats['Value'].items()]
        
        table1 = ax1.table(cellText=general_data,
                          colLabels=['Metric', 'Value'],
                          cellLoc='left',
                          loc='upper center',
                          bbox=[0.1, 0.5, 0.8, 0.4])
        table1.auto_set_font_size(False)
        table1.set_fontsize(10)
        table1.scale(1, 2)
        
        # Style header
        for i in range(2):
            table1[(0, i)].set_facecolor('#4472C4')
            table1[(0, i)].set_text_props(weight='bold', color='white')
        
        # Overall Statistics
        ax2.axis('tight')
        ax2.axis('off')
        ax2.set_title('Overall Engagement Statistics', fontsize=14, fontweight='bold', pad=20)
        
        overall_data = [[idx] + [f"{val:,.2f}" for val in row] 
                       for idx, row in overall_stats.iterrows()]
        
        table2 = ax2.table(cellText=overall_data,
                          colLabels=['Metric', 'Mean', 'Median', 'Std Dev', 'Min', 'Max', 'Total'],
                          cellLoc='right',
                          loc='upper center',
                          bbox=[0.05, 0.3, 0.9, 0.6])
        table2.auto_set_font_size(False)
        table2.set_fontsize(9)
        table2.scale(1, 2)
        
        # Style header
        for i in range(7):
            table2[(0, i)].set_facecolor('#4472C4')
            table2[(0, i)].set_text_props(weight='bold', color='white')
        
        # Alternate row colors
        for i in range(1, len(overall_data) + 1):
            if i % 2 == 0:
                for j in range(7):
                    table2[(i, j)].set_facecolor('#E7E6E6')
        
        plt.tight_layout()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()
        
        # Page 2: Party Statistics
        fig, ax = plt.subplots(figsize=(11, 14))
        fig.suptitle('Table 1 (continued): Statistics by Party', 
                     fontsize=16, fontweight='bold', y=0.98)
        
        ax.axis('tight')
        ax.axis('off')
        
        # Prepare party data
        party_data = []
        for idx, row in party_stats.iterrows():
            party_data.append([
                idx,
                f"{row['Video Count']:.0f}",
                f"{row['data.stats.playCount_mean']:,.0f}",
                f"{row['data.stats.playCount_sum']:,.0f}",
                f"{row['data.stats.diggCount_mean']:,.0f}",
                f"{row['data.stats.diggCount_sum']:,.0f}",
                f"{row['data.stats.commentCount_mean']:,.0f}",
                f"{row['data.stats.commentCount_sum']:,.0f}",
                f"{row['data.stats.shareCount_mean']:,.0f}",
                f"{row['data.stats.shareCount_sum']:,.0f}",
            ])
        
        col_labels = ['Party', 'Videos', 'Avg\nPlays', 'Total\nPlays', 
                     'Avg\nLikes', 'Total\nLikes', 'Avg\nComments', 
                     'Total\nComments', 'Avg\nShares', 'Total\nShares']
        
        table3 = ax.table(cellText=party_data,
                         colLabels=col_labels,
                         cellLoc='right',
                         loc='upper center',
                         bbox=[0.02, 0.3, 0.96, 0.6])
        table3.auto_set_font_size(False)
        table3.set_fontsize(8)
        table3.scale(1, 2.5)
        
        # Style header
        for i in range(len(col_labels)):
            table3[(0, i)].set_facecolor('#4472C4')
            table3[(0, i)].set_text_props(weight='bold', color='white')
        
        # Alternate row colors
        for i in range(1, len(party_data) + 1):
            if i % 2 == 0:
                for j in range(len(col_labels)):
                    table3[(i, j)].set_facecolor('#E7E6E6')
        
        # Make party names bold
        for i in range(1, len(party_data) + 1):
            table3[(i, 0)].set_text_props(weight='bold')
        
        plt.tight_layout()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()
        
        # Add metadata
        d = pdf.infodict()
        d['Title'] = 'Table 1: TikTok Data Descriptive Statistics'
        d['Author'] = 'Research Team'
        d['Subject'] = 'TikTok Political Party Analysis'
        d['CreationDate'] = pd.Timestamp.now()

def main():
    """Main execution function"""
    print("Loading TikTok data from CSV files...")
    df = load_all_data()
    print(f"Loaded {len(df)} videos from {df['party'].nunique()} parties")
    
    print("\nCreating descriptive statistics...")
    overall_stats, general_stats, party_stats = create_descriptive_table(df)
    
    print("\nGenerating PDF table...")
    create_pdf_table(overall_stats, general_stats, party_stats, OUTPUT_PDF)
    
    print(f"\n✓ Table 1 successfully created: {OUTPUT_PDF}")
    print("\nSummary:")
    print(general_stats)
    print("\n" + "="*80)
    print("\nParty Overview:")
    print(party_stats[['Video Count', 'data.stats.playCount_sum', 'data.stats.diggCount_sum']])

if __name__ == "__main__":
    main()
