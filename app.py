from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# 🔑 RapidAPI credentials
RAPID_API_KEY = "b06c1d49b6msh245e5212bde725ap1c5f2ajsnf1a181d58373"
RAPID_API_HOST = "instagram-downloader-scraper-reels-igtv-posts-stories.p.rapidapi.com"

@app.route("/", methods=["GET"])
def home():
    return "Backend is live ✅"

@app.route("/download", methods=["POST"])
def download():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({
            "status": "error",
            "message": "Instagram URL required"
        }), 400

    try:
        response = requests.get(
            "https://instagram-downloader-scraper-reels-igtv-posts-stories.p.rapidapi.com/media",
            headers={
                "X-RapidAPI-Key": RAPID_API_KEY,
                "X-RapidAPI-Host": RAPID_API_HOST
            },
            params={
                "url": url
            },
            timeout=30
        )

        result = response.json()

        # 🔍 Extract video URL (API returns array sometimes)
        if "media" in result and len(result["media"]) > 0:
            video_url = result["media"][0].get("url")

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
