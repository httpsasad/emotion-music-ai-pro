import sys
import os
import json
import pandas as pd

# Add current directory to path
sys.path.append(os.getcwd())

from backend.text_emotion import predict_emotion
from backend.recommender import recommend_songs

def test_flow():
    test_inputs = ["feeling badmoshi", "romantic date", "feeling very sad", "purane gane"]
    
    print("--- STARTING END-TO-END SANITY SHUTD- CHECK ---")
    
    for text in test_inputs:
        print(f"\n[INPUT]: {text}")
        
        # 1. Prediction
        try:
            emotion = predict_emotion(text)
            print(f"  [EMOTION]: {emotion}")
        except Exception as e:
            print(f"  [ERROR-PREDICTION]: {e}")
            continue
            
        # 2. Recommendation
        try:
            songs = recommend_songs(emotion)
            print(f"  [SONGS FOUND]: {len(songs)}")
            if len(songs) == 0:
                print("  [ERROR]: No songs found for this emotion!")
                continue
            
            # 3. HTML Injection Prep
            tracks = songs.to_dict('records')
            tracks_json = json.dumps(tracks)
            
            # Verify basic structure
            if 'youtube_id' not in tracks[0]:
                print("  [ERROR]: youtube_id column missing in songs.csv!")
                
        except Exception as e:
            print(f"  [ERROR-RECOM]: {e}")
            
    print("\n[TEMPLATE CHECK]:")
    if os.path.exists('backend/player_template.html'):
        with open('backend/player_template.html', 'r', encoding='utf-8') as f:
            content = f.read()
            if '[TRACKS_JSON]' in content:
                print("  [OK]: Player template has [TRACKS_JSON] placeholder.")
            else:
                print("  [ERROR]: Player template missing [TRACKS_JSON] placeholder!")
    else:
        print("  [ERROR]: player_template.html MISSING!")

    print("\n--- SANITY CHECK COMPLETE ---")

if __name__ == "__main__":
    test_flow()
