import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
from typing import Dict, Any

# --- Universal Configuration ---

# Define the ABSOLUTE target output directory for charts and aggregated CSVs
OUTPUT_DIR = '1_Processing/2_Analysis/3_Label_Posts_Voting_Topic'

# Define the column containing the labels (0, 1, 2, 3)
LABEL_COLUMN = 'voting.topic'
# The column we will create to store the party name extracted from the filename
PARTY_COLUMN = 'party_name'

# Define the platform-specific configurations
PLATFORM_CONFIGS: Dict[str, Dict[str, Any]] = {
    "Tiktok": {
        "DATA_PATH": 'A_Data/1_Tiktok/2_CLEAN'
    },
    "Instagram": {
        "DATA_PATH": 'A_Data/2_Instagram/2_CLEAN'
    }
}

# Define mapping for topic labels for better readability in the legend
TOPIC_MAPPING = {
    0: '0: Not a voting topic',
    1: '1: E-ID',
    2: '2: Eigenmietwert',
    3: '3: Both (E-ID & Eigenmietwert)'
}

# --- Unified Processing Function ---

def aggregate_and_plot_data(platform_name: str, directory: str, output_dir: str):
    """
    Reads all CSV files, extracts party name from the filename, aggregates topic 
    counts by party, and generates a bar chart, saving output to the specified absolute directory.
    """
    search_path = os.path.join(directory, '*.csv')
    csv_files = glob.glob(search_path)
    
    # Ensure the output directory exists
    # This is crucial for absolute paths
    os.makedirs(output_dir, exist_ok=True)
    
    if not csv_files:
        print(f"No CSV files found in the directory for {platform_name}: {directory}")
        return

    print(f"Processing {platform_name} data: {len(csv_files)} files found.")

    # 1. Read, Extract Party Name, and Concatenate DataFrames
    all_dfs = []
    for file_path in csv_files:
        try:
            filename = os.path.basename(file_path)
            # Extract the full filename without the .csv extension for the label
            party_name = os.path.splitext(filename)[0]
            
            df = pd.read_csv(file_path)
            
            df[PARTY_COLUMN] = party_name
            all_dfs.append(df)
            
        except Exception as e:
            print(f"Error reading {os.path.basename(file_path)}: {e}")
            
    if not all_dfs:
        print(f"No usable data found for {platform_name}.")
        return

    df_platform = pd.concat(all_dfs, ignore_index=True)

    if LABEL_COLUMN not in df_platform.columns:
        print(f"Required column ('{LABEL_COLUMN}') not found in {platform_name} data. Skipping.")
        return

    # 2. Aggregate Data
    df_platform[LABEL_COLUMN] = pd.to_numeric(df_platform[LABEL_COLUMN], errors='coerce').fillna(0).astype(int)
    
    aggregated_counts = (
        df_platform.groupby([PARTY_COLUMN, LABEL_COLUMN])
        .size()
        .unstack(fill_value=0)
    )

    available_topics = [t for t in [0, 1, 2, 3] if t in aggregated_counts.columns]
    plot_data = aggregated_counts[available_topics].rename(columns=TOPIC_MAPPING)
    
    # Save aggregated data to CSV in the specified output directory
    output_csv_filename = f'{platform_name.lower()}_topic_counts_by_file.csv'
    output_csv_file = os.path.join(output_dir, output_csv_filename)
    plot_data.to_csv(output_csv_file)
    print(f"Aggregated data saved to {output_csv_file}")

    # 3. Generate and Save Bar Chart (Manual Matplotlib Control)
    fig, ax = plt.subplots(figsize=(12, 8))
    
    plot_data.plot(kind='bar', stacked=True, ax=ax)
    
    # Explicitly set the x-tick labels to the index (party names/filenames)
    ax.set_xticklabels(plot_data.index.values, rotation=45, ha='right')
    
    ax.set_title(f'Count of Posts by Topic and CSV File Name on {platform_name}', fontsize=16)
    ax.set_xlabel('CSV File Name (Party)', fontsize=14) 
    ax.set_ylabel('Number of Posts', fontsize=14)
    
    # Place legend outside of the plot
    ax.legend(title='Voting Topic', bbox_to_anchor=(1.05, 1), loc='upper left')
    fig.tight_layout(rect=[0, 0, 0.85, 1])
    
    # Save the chart to the specified output directory
    output_image_filename = f'{platform_name.lower()}_topic_counts.png'
    output_image_file = os.path.join(output_dir, output_image_filename)
    fig.savefig(output_image_file)
    plt.close(fig)
    print(f"Bar chart saved to {output_image_file}")

# --- Main Execution Block ---

if __name__ == "__main__":
    print("--- Starting Post Label Aggregation and Plotting ---")
    
    # Process both platforms
    for platform, config in PLATFORM_CONFIGS.items():
        print("-" * 50)
        aggregate_and_plot_data(
            platform_name=platform,
            directory=config['DATA_PATH'],
            output_dir=OUTPUT_DIR
        )
        
    print("\nAll platforms have been processed and charts generated.")