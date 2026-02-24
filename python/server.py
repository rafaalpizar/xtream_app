from flask import Flask, request, jsonify
import sqlite3
from config import SERVER_USER, SERVER_PASS

app = Flask(__name__)
DB_FILE = "streams.db"

def check_auth(username, password):
    return username == SERVER_USER and password == SERVER_PASS

@app.route("/streams", methods=["GET"])
def get_streams():
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return jsonify({"error": "Unauthorized"}), 401

    stream_type = request.args.get("type")  # live/vod/series
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    if stream_type:
        c.execute("SELECT name, category, type, url FROM streams WHERE type=?", (stream_type,))
    else:
        c.execute("SELECT name, category, type, url FROM streams")
    rows = c.fetchall()
    conn.close()

    return jsonify([{"name": r[0], "category": r[1], "type": r[2], "url": r[3]} for r in rows])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
