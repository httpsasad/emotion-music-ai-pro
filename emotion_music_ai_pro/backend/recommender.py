import pandas as pd

def recommend_songs(emotion):
    try:
        df = pd.read_csv("data/songs.csv")
        # Filter for the specific mood
        mood_df = df[df["mood"].str.lower() == str(emotion).lower()]
        
        if mood_df.empty:
            return pd.DataFrame()
            
        # Sample up to 6 songs for the grid
        count = min(6, len(mood_df))
        results = mood_df.sample(count)
        return results
    except Exception as e:
        print(f"Recommender Error: {e}")
        return pd.DataFrame()
