import ndjson
import pandas as pd
from pandas import json_normalize
import os
import re

def preptiktok_through_user(file_name, date_a, date_b):
    with open(file_name, 'r') as f:
        data = ndjson.load(f)

    df_flat = json_normalize(data)

    columns_to_select = [
        'source_platform', 'source_platform_url', 'data.id', 'data.desc',
        'data.createTime', 'data.stats.collectCount', 'data.stats.commentCount',
        'data.stats.diggCount', 'data.stats.playCount', 'data.stats.shareCount',
        'data.author.nickname', 'data.author.id', 'data.duetDisplay',
        'data.duetEnabled', 'data.author.signature', 'data.author.uniqueId'
    ]

    df_small = df_flat.loc[:, columns_to_select]
    df_small.loc[:, 'video_url'] = (
        "https://www.tiktok.com/@" + df_small['data.author.uniqueId'] + "/video/" + df_small['data.id']
    )

    df_small['data.createTime'] = pd.to_datetime(df_small['data.createTime'], unit='s')
    date_a = pd.to_datetime(date_a)
    date_b = pd.to_datetime(date_b)
    df_small = df_small[(df_small['data.createTime'] >= date_a) & (df_small['data.createTime'] <= date_b)]

    return df_small


### Clean files

raw_dir = "/Users/nickeichmann/PythonProjects/Introduction-to-Computational-Media-Research/A_Data/1_Tiktok/1_RAW"
clean_dir = "/Users/nickeichmann/PythonProjects/Introduction-to-Computational-Media-Research/A_Data/1_Tiktok/2_CLEAN"

os.makedirs(clean_dir, exist_ok=True)

for file in os.listdir(raw_dir):
    filename = os.fsdecode(file)
    file_path = os.path.join(raw_dir, filename)

    print(f"Processing {filename}...")

    return_df = preptiktok_through_user(file_path, "2025-03-09", "2025-10-12")

    save_path = os.path.join(clean_dir, filename.split('Tiktok')[0] + "_cleaned.csv")
    return_df.to_csv(save_path, index=False)

print("✅ All done!")
