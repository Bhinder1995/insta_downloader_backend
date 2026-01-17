from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# ==============================
# RapidAPI Configuration
# ==============================
RAPID_API_KEY = os.getenv("RAPID_API_KEY")
RAPID_API_HOST = "instagram-downloader-scraper-reels-igtv-posts-stories.p.rapidapi.com"
RAPID_API_URL = "https://instagram-downloader-scraper-reels-igtv-posts-stories.p.rapidapi.com/media"

# ==============================
# Health Check
# ==============================
@app.route("/", methods=["GET"])
def home():
    return "Backend is live ✅"

# ==============================
# Download Endpoint
# ==============================
@app.route("/download", methods=["POST"])
def download():
    data = request.get_json()
    url = data.get("url") if data else None

    if not url:
        return jsonify({
            "status": "error",
            "message": "Instagram URL required"
        }), 400

    try:
        response = requests.get(
            RAPID_API_URL,
            headers={
                "X-RapidAPI-Key": RAPID_API_KEY,
                "X-RapidAPI-Host": RAPID_API_HOST
            },
            params={"url": url},
            timeout=30
        )

        result = response.json()

        # ==============================
        # ROBUST VIDEO URL EXTRACTION
        # ==============================
        video_url = None

        # Format 1: { media: [{ url }] }
        if isinstance(result, dict) and "media" in result:
            if isinstance(result["media"], list) and len(result["media"]) > 0:
                video_url = result["media"][0].get("url")

        # Format 2: { data: { video_url } }
        if not video_url and isinstance(result, dict) and "data" in result:
            if isinstance(result["data"], dict):
                video_url = result["data"].get("video_url")

        # Format 3: { result: [{ type: "video", url }] }
        if not video_url and isinstance(result, dict) and "result" in result:
            if isinstance(result["result"], list):
                for item in result["result"]:
                    if item.get("type") == "video":
                        video_url = item.get("url")
                        break

        # ==============================
        # FINAL RESPONSE
        # ==============================
        if video_url:
            return jsonify({
                "status": "success",
                "video_url": video_url
            })

        return jsonify({
            "status": "error",
            "message": "Video not found"
        }), 400

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Download failed"
        }), 500


# ==============================
# Run App
# ==============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
