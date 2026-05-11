import streamlit as st
import json
import os
from backend.text_emotion import predict_emotion
from backend.recommender import recommend_songs
from backend.face_emotion import detect_emotion_from_face
import streamlit.components.v1 as components

# --- PAGE CONFIG ---
st.set_page_config(page_title="VIBE ELITE | Professional Audio Experience", layout="wide")

# --- CUSTOM THEME (MATTE BLACK PROFESSIONAL) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700;900&family=Outfit:wght@300;400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
        background-color: #000000 !important;
        color: white;
    }

    .main {
        background-color: #000000 !important;
    }

    .hero-title {
        font-family: 'Montserrat', sans-serif;
        font-size: 4.5rem;
        font-weight: 900;
        text-align: center;
        margin-top: 40px;
        margin-bottom: 0;
        letter-spacing: -3px;
        color: #FFFFFF;
    }

    .status-bar {
        text-align: center;
        color: #1DB954; /* Spotify Green */
        text-transform: uppercase;
        letter-spacing: 4px;
        font-weight: 700;
        margin-bottom: 40px;
        font-size: 0.8rem;
    }

    /* Professional Sidebar */
    [data-testid="stSidebar"] {
        background: #0a0a0a;
        border-right: 1px solid #1a1a1a;
    }

    /* Button Polish */
    .stButton > button {
        background: #1DB954 !important;
        border: none !important;
        color: black !important;
        border-radius: 4px !important;
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 800 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='font-family: Montserrat;'>ELITE SYSTEM</h2>", unsafe_allow_html=True)
    st.markdown("---")
    mode = st.radio("SELECT ENGINE", ["NEURAL TEXT 💬", "FACIAL SCANNER 📷"])
    st.markdown("<br><br>", unsafe_allow_html=True)

# --- MAIN UI ---
st.markdown('<div class="hero-title">VIBE ELITE AI</div>', unsafe_allow_html=True)
st.markdown('<div class="status-bar">Premium Audio Recommendation Engine</div>', unsafe_allow_html=True)

emotion = None

if mode.startswith("NEURAL"):
    user_input = st.text_input("How are you feeling?", placeholder="e.g. badmoshi, romantic mood, gussa...", key="main_text_input")
    if user_input:
        emotion = predict_emotion(user_input)
else:
    if st.button("INITIALIZE BIOMETRIC SCAN", key="face_scan_btn"):
        with st.status("Analyzing Facial Features...", expanded=True) as status:
            st.write("🔍 Locating facial landmarks...")
            st.write("🧬 Processing biometric ratios...")
            emotion = detect_emotion_from_face()
            st.write(f"✅ Neural classification complete: {emotion.upper()}")
            status.update(label="Scan Successful!", state="complete", expanded=False)

# --- AUDIO PLAYER CORE ---
if emotion:
    st.markdown(f"### CURRENT STATE: <span style='color: #58a6ff;'>{emotion.upper()}</span>", unsafe_allow_html=True)
    
    # Get recommendations
    songs_df = recommend_songs(emotion)
    
    if songs_df.empty:
        st.warning(f"No songs found for mood: {emotion}. Try typing something else!")
    else:
        tracks_raw = songs_df.to_dict('records')
        import math
        tracks = []
        for t in tracks_raw:
            cleaned_t = {k: (None if isinstance(v, float) and math.isnan(v) else v) for k, v in t.items()}
            tracks.append(cleaned_t)
            
        # Render Custom Player
        try:
            with open('backend/player_template.html', 'r', encoding='utf-8') as f:
                template = f.read()
            
            # Inject Data
            tracks_json = json.dumps(tracks)
            # Use safer replacement and JSON parsing in JS
            html_code = template.replace('TRACKS_JSON_PLACEHOLDER', tracks_json)
            
            # Display Component via Streamlit's built-in iframe handler so tags aren't stripped
            components.html(html_code, height=1000, scrolling=True)
        except Exception as e:
            st.error(f"Engine Error: {e}")

# --- FOOTER ---
st.markdown("""
<div style="position: fixed; bottom: 20px; left: 0; right: 0; text-align: center; color: rgba(255,255,255,0.2); font-size: 0.8rem; letter-spacing: 2px;">
    POWERED BY VIBE ELITE AI &bull; ADVANCED AUDIO RECOMMENDATION &bull; 2026
</div>
""", unsafe_allow_html=True)
