import pandas as pd
import urllib.request
import urllib.parse
import re
import time

songs_data = [
    # Happy
    ("Chaleya", "Arijit Singh", "happy"),
    ("Badtameez Dil", "Benny Dayal", "happy"),
    ("Ghungroo", "Arijit Singh", "happy"),
    ("Aankh Marey", "Neha Kakkar", "happy"),
    ("Desi Girl", "Shankar Mahadevan", "happy"),
    ("Subha Hone Na De", "Mika Singh", "happy"),
    
    # Sad
    ("Channa Mereya", "Arijit Singh", "sad"),
    ("Luka Chuppi", "A.R. Rahman", "sad"),
    ("Agar Tum Saath Ho", "Arijit Singh", "sad"),
    ("Kabira", "Arijit Singh", "sad"),
    ("Tujhe Bhula Diya", "Mohit Chauhan", "sad"),
    ("Bhula Dena", "Mustafa Zahid", "sad"),
    
    # Relaxed
    ("Kun Faya Kun", "A.R. Rahman", "relaxed"),
    ("Tum Hi Ho", "Arijit Singh", "relaxed"),
    ("Iktara", "Kavita Seth", "relaxed"),
    ("Tum Se Hi", "Mohit Chauhan", "relaxed"),
    ("Pehli Nazar Mein", "Atif Aslam", "relaxed"),
    ("Raabta", "Arijit Singh", "relaxed"),
    
    # Badmoshi (Attitude/Swag)
    ("Apna Time Aayega", "Ranveer Singh", "badmoshi"),
    ("Kala Chashma", "Badshah", "badmoshi"),
    ("Sher Khul Gaye", "Vishal Dadlani", "badmoshi"),
    ("Zinda", "Siddharth Mahadevan", "badmoshi"),
    ("Kar Gayi Chull", "Badshah", "badmoshi"),
    ("Aarambh Hai Prachand", "Piyush Mishra", "badmoshi"),
    
    # Classic
    ("Lag Ja Gale", "Lata Mangeshkar", "classic"),
    ("Pal Pal Dil Ke Paas", "Kishore Kumar", "classic"),
    ("Kya Hua Tera Wada", "Mohammed Rafi", "classic"),
    ("Mere Sapno Ki Rani", "Kishore Kumar", "classic"),
    ("Gulabi Aankhen", "Mohammed Rafi", "classic"),
    ("Chura Liya Hai Tumne", "Asha Bhosle", "classic"),
    
    # Funny / Party
    ("Bhootni Ke", "Daler Mehndi", "funny"),
    ("Character Dheela", "Neeraj Shridhar", "funny"),
    ("Ullu Ka Pattha", "Arijit Singh", "funny"),
    ("Lungi Dance", "Yo Yo Honey Singh", "funny"),
    ("Tinku Jiya", "Mamta Sharma", "funny"),
    ("Aunty Ji", "Ash King", "funny"),
    
    # Romantic
    ("Tera Ban Jaunga", "Akhil Sachdeva", "romantic"),
    ("Pee Loon", "Mohit Chauhan", "romantic"),
    ("Tu Jaane Na", "Atif Aslam", "romantic"),
    ("Kesariya", "Arijit Singh", "romantic"),
    ("Zehnaseeb", "Chinmayi Sripaada", "romantic"),
    ("Tujh Mein Rab Dikhta Hai", "Roop Kumar Rathod", "romantic")
]

rows = []

for song, artist, mood in songs_data:
    query = f"{song} {artist} official audio"
    vid = ""
    try:
        q = urllib.parse.quote(query)
        req = urllib.request.Request('https://www.youtube.com/results?search_query='+q, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req).read().decode('utf-8')
        video_ids = re.findall(r'"videoId":"([a-zA-Z0-9_-]{11})"', html)
        if video_ids:
            vid = video_ids[0]
            print(f"Found {vid} for {song}")
        time.sleep(0.3)
    except Exception as e:
        print(f"Error fetching {song}: {e}")
        
    rows.append({
        'song': song,
        'artist': artist,
        'mood': mood,
        'youtube_id': vid,
        'duration': '3:30',
        'spotify_id': '',
        'preview_url': ''
    })

df = pd.DataFrame(rows)
df.to_csv('data/songs.csv', index=False)
print("SUCCESS: Hindi songs saved.")
