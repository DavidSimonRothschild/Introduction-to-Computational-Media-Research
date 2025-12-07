import pandas as pd
import os
import glob

#vlt basic topic modeling um themen cluster zu identifizieren und word frequency um herauszufinden was noch dazuzählen könnte - erleichtert einordnung
# vlt diese auch noch ein label geben:  "abstimmung", "stimmen", "stimmt", "volksabstimmung"
# --- TIKTOK DATA ---


# --- Configuration ---
# Define the path where your CSV files are located
DATA_PATH = 'A_Data/1_Tiktok/2_CLEAN'
# Define the column to search in
TEXT_COLUMN = 'data.desc'
# Define the new column to be added
LABEL_COLUMN = 'voting.topic'



# Define a dictionary where keys are the labels and values are lists of keywords
# All keywords must be in lowercase.
TOPIC_KEYWORDS = {
    # Label 1: E-ID
    1: ["e-id", "eid", "e id", "elektronische identität", "privatsphäre", "überwachung"],
    
    # Label 2: Eigenmietwert
    2: ["eigenmietwert", "mietwert", "wohneigentumsbesteuerung", "eigenmietwertbesteuerung"]
}

def label_data_topic(text):
    """
    Checks the text for voting topics and assigns a label:
    - 3 if keywords for BOTH Topic 1 (E-ID) and Topic 2 (Eigenmietwert) are present.
    - 1 if only Topic 1 keywords are present.
    - 2 if only Topic 2 keywords are present.
    - 0 if neither are present.
    """
    if pd.isna(text):
        # Handle NaN/missing values
        return 0
    
    # Convert the text to lowercase for case-insensitive checking
    text_lower = str(text).lower()
    
    # --- Step 1: Check for the presence of each topic individually ---
    
    # Check if ANY keyword for Topic 1 (E-ID) is in the text
    topic_1_present = any(keyword in text_lower for keyword in TOPIC_KEYWORDS.get(1, []))
    
    # Check if ANY keyword for Topic 2 (Eigenmietwert) is in the text
    topic_2_present = any(keyword in text_lower for keyword in TOPIC_KEYWORDS.get(2, []))
    
    # --- Step 2: Assign the final label based on the presence check ---

    # 1. If BOTH are present, return 3
    if topic_1_present and topic_2_present:
        return 3
    
    # 2. If ONLY Topic 1 is present, return 1
    elif topic_1_present:
        return 1
    
    # 3. If ONLY Topic 2 is present, return 2
    elif topic_2_present:
        return 2
    
    # 4. If neither is present, return 0
    else:
        return 0

def process_csv_files(directory):
    """
    Finds all CSV files in the given directory and applies the labeling function 
    to the specified column, then overwrites the original file.
    """
    # Use glob to find all files ending with .csv in the directory
    search_path = os.path.join(directory, '*.csv')
    csv_files = glob.glob(search_path)
    
    if not csv_files:
        print(f"⚠️ No CSV files found in the directory: {directory}")
        return

    print(f"📂 Found {len(csv_files)} CSV files. Starting processing...")

    for file_path in csv_files:
        print(f"\n--- Processing: {os.path.basename(file_path)} ---")
        
        try:
            # 1. Read the CSV file
            df = pd.read_csv(file_path)
            
            # Check if the required column exists
            if TEXT_COLUMN not in df.columns:
                print(f"❌ Column '{TEXT_COLUMN}' not found in the file. Skipping.")
                continue

            # 2. Apply the labeling function to the specified column
            df[LABEL_COLUMN] = df[TEXT_COLUMN].apply(label_data_topic)
            
            # 3. Save the modified DataFrame back to the original file
            df.to_csv(file_path, index=False)
            
            print(f"✅ Successfully added/updated '{LABEL_COLUMN}' column and saved the file.")
            
        except Exception as e:
            print(f"🚨 An error occurred while processing {os.path.basename(file_path)}: {e}")

# --- Main execution block ---
if __name__ == "__main__":
    process_csv_files(DATA_PATH)
    print("\n🚀 All CSV files have been processed.")



# --- INSTAGRAM DATA ---

# --- Configuration ---
# Define the path where your CSV files are located
DATA_PATH = 'A_Data/2_Instagram/2_CLEAN'
# Define the column to search in
TEXT_COLUMN = 'data.caption.text'
# Define the new column to be added
LABEL_COLUMN = 'voting.topic'

# Define a dictionary where keys are the labels and values are lists of keywords
# All keywords must be in lowercase.

TOPIC_KEYWORDS = {
    # Label 1: E-ID
    1: ["e-id", "eid", "e id", "elektronische identität", "privatsphäre", "überwachung"],
    
    # Label 2: Eigenmietwert
    2: ["eigenmietwert", "mietwert", "wohneigentumsbesteuerung", "eigenmietwertbesteuerung"]
}


def label_data_topic(text):
    """
    Checks the text for voting topics and assigns a label:
    - 3 if keywords for BOTH Topic 1 (E-ID) and Topic 2 (Eigenmietwert) are present.
    - 1 if only Topic 1 keywords are present.
    - 2 if only Topic 2 keywords are present.
    - 0 if neither are present.
    """
    if pd.isna(text):
        # Handle NaN/missing values
        return 0
    
    # Convert the text to lowercase for case-insensitive checking
    text_lower = str(text).lower()
    
    # --- Step 1: Check for the presence of each topic individually ---
    
    # Check if ANY keyword for Topic 1 (E-ID) is in the text
    topic_1_present = any(keyword in text_lower for keyword in TOPIC_KEYWORDS.get(1, []))
    
    # Check if ANY keyword for Topic 2 (Eigenmietwert) is in the text
    topic_2_present = any(keyword in text_lower for keyword in TOPIC_KEYWORDS.get(2, []))
    
    # --- Step 2: Assign the final label based on the presence check ---

    # 1. If BOTH are present, return 3
    if topic_1_present and topic_2_present:
        return 3
    
    # 2. If ONLY Topic 1 is present, return 1
    elif topic_1_present:
        return 1
    
    # 3. If ONLY Topic 2 is present, return 2
    elif topic_2_present:
        return 2
    
    # 4. If neither is present, return 0
    else:
        return 0

def process_csv_files(directory):
    """
    Finds all CSV files in the given directory and applies the labeling function 
    to the specified column, then overwrites the original file.
    """
    # Use glob to find all files ending with .csv in the directory
    search_path = os.path.join(directory, '*.csv')
    csv_files = glob.glob(search_path)
    
    if not csv_files:
        print(f"⚠️ No CSV files found in the directory: {directory}")
        return

    print(f"📂 Found {len(csv_files)} CSV files. Starting processing...")

    for file_path in csv_files:
        print(f"\n--- Processing: {os.path.basename(file_path)} ---")
        
        try:
            # 1. Read the CSV file
            df = pd.read_csv(file_path)
            
            # Check if the required column exists
            if TEXT_COLUMN not in df.columns:
                print(f"❌ Column '{TEXT_COLUMN}' not found in the file. Skipping.")
                continue

            # 2. Apply the labeling function to the specified column
            df[LABEL_COLUMN] = df[TEXT_COLUMN].apply(label_data_topic)
            
            # 3. Save the modified DataFrame back to the original file
            df.to_csv(file_path, index=False)
            
            print(f"✅ Successfully added/updated '{LABEL_COLUMN}' column and saved the file.")
            
        except Exception as e:
            print(f"🚨 An error occurred while processing {os.path.basename(file_path)}: {e}")

# --- Main execution block ---
if __name__ == "__main__":
    process_csv_files(DATA_PATH)
    print("\n🚀 All CSV files have been processed.")

