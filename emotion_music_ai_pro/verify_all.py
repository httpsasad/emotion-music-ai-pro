from backend.text_emotion import predict_emotion
from backend.recommender import recommend_songs

emotions_to_test = ["badmoshi vibe", "pure classic", "hansao mujhe", "romantic feeling", "gangstar music"]

for text in emotions_to_test:
    emotion = predict_emotion(text)
    print(f"Text: '{text}' -> Predicted: {emotion}")
    songs = recommend_songs(emotion)
    print(f"   Songs recommended: {len(songs)}")
    for _, row in songs.iterrows():
        print(f"   - {row['song']} | {row['link']}")
    print("-" * 30)
