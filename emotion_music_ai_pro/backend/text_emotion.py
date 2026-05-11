from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Dictionary-based training data for better maintainability and fewer manual errors
data = {
    "happy": ["I am happy", "I feel great", "main khush hoon", "aaj maza aa gaya", "feeling awesome", "so happy", "zindabad", "very good"],
    "sad": ["I feel sad", "I am depressed", "mujhe udaasi hai", "dukhi hoon main", "feeling low", "rona aa raha", "dil tut gaya", "sad mood"],
    "angry": ["I am angry", "I am frustrated", "mujhe gussa hai", "dimag kharab hai", "shut up", "gussa", "pagal ho gaya", "very angry"],
    "relaxed": ["I feel calm", "I am relaxed", "main relax hoon", "skoon hai", "peaceful", "shanti", "relax mode", "chill", "sukoon"],
    "badmoshi": ["badmoshi", "gangster vibe", "sidhu moose wala", "cheema y", "system", "daku", "attitude", "badmash", "gangstar music", "badmashi gaany", "attitue wali video", "gangster style", "shubh"],
    "classic": ["classic", "purany gaany", "old is gold", "old songs", "kishore kumar", "lata mangeshkar", "purana style", "purane gane", "90s music", "retro hits", "classic vibes"],
    "funny": ["funny", "joke", "mazak", "hansna", "laugh", "comedy", "mazahiya", "hansao mujhe", "comedy songs", "funny vibes", "funny scene"],
    "romantic": ["romantic", "love", "pyaar", "ishq", "mohabat", "dil", "sweet", "couple", "romantic mood", "pyar wali video", "love songs", "romantic feelings"]
}

texts = []
labels = []

for label, phrases in data.items():
    for phrase in phrases:
        texts.append(phrase)
        labels.append(label)

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

model = LogisticRegression()
model.fit(X, labels)

def predict_emotion(text):
    if not text:
        return "happy"
    try:
        return model.predict(vectorizer.transform([str(text).lower()]))[0]
    except Exception:
        return "happy"
