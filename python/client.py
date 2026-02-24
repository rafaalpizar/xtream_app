import requests
import sqlite3
import schedule
import time
from config import XTREAM_URL, USERNAME, PASSWORD, WHITELIST, BLACKLIST

DB_FILE = "streams.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS streams (
            id INTEGER PRIMARY KEY,
            name TEXT,
            category TEXT,
            type TEXT,
            url TEXT
        )
    """)
    conn.commit()
    conn.close()

def fetch_streams():
    auth = {"username": USERNAME, "password": PASSWORD}
    resp = requests.get(f"{XTREAM_URL}/player_api.php", params=auth)
    resp.raise_for_status()
    data = resp.json()
    return data

def filter_streams(data):
    filtered = []
    for stream_type in ["live", "vod", "series"]:
        for s in data.get(f"{stream_type}_streams", []):
            name, category = s.get("name"), s.get("category_name")
            if (name in WHITELIST or category in WHITELIST) and \
               (name not in BLACKLIST and category not in BLACKLIST):
                filtered.append({
                    "name": name,
                    "category": category,
                    "type": stream_type,
                    "url": s.get("stream_url")
                })
    return filtered

def store_streams(streams):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM streams")  # refresh daily
    for s in streams:
        c.execute("INSERT INTO streams (name, category, type, url) VALUES (?, ?, ?, ?)",
                  (s["name"], s["category"], s["type"], s["url"]))
    conn.commit()
    conn.close()

def refresh():
    print(f"Refreshing streams from {XTREAM_URL}...")
    streams = []
    try:
        data = fetch_streams()
        streams = filter_streams(data)
        store_streams(streams)
    except Exception as ex:
    	print("%s" % ex)
        
    print(f"Stored {len(streams)} streams.")

if __name__ == "__main__":
    init_db()
    refresh()
    schedule.every().day.at("03:00").do(refresh)  # daily refresh
    while True:
        schedule.run_pending()
        time.sleep(60)
