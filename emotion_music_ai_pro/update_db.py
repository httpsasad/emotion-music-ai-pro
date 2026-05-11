import pandas as pd
import urllib.request
import urllib.parse
import re
import time

df = pd.read_csv('data/songs.csv')
cache = {}

for idx, row in df.iterrows():
    if pd.notna(row['youtube_id']) and str(row['youtube_id']).strip():
        continue
    
    # Extract base song name without " (Mix X)"
    song_name = re.sub(r' \(Mix \d+\)', '', str(row['song']))
    artist = str(row['artist'])
    query = f"{song_name} {artist} audio"
    
    if query in cache:
        df.at[idx, 'youtube_id'] = cache[query]
        print(f"Skipped {query} (cached)")
        continue
        
    try:
        q = urllib.parse.quote(query)
        req = urllib.request.Request('https://www.youtube.com/results?search_query='+q, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req).read().decode('utf-8')
        video_ids = re.findall(r'"videoId":"([a-zA-Z0-9_-]{11})"', html)
        if video_ids:
            vid = video_ids[0]
            df.at[idx, 'youtube_id'] = vid
            cache[query] = vid
            print(f"Found {vid} for {query}")
        else:
            print(f"No match for {query}")
        time.sleep(0.5)
    except Exception as e:
        print(f"Error for {query}: {e}")

df.to_csv('data/songs.csv', index=False)
print("Updated database to data/songs.csv")
