import urllib.request
import re

html = urllib.request.urlopen("https://kworb.net/spotify/country/in_weekly.html").read().decode("utf-8")
links = re.findall(r'href="\.\./track/(.*?)\.html">(.*?)</a>', html)

for track_id, title in links[:100]:
    print(f"{track_id} | {title}")
