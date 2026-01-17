from flask import Flask, request, jsonify
from flask_cors import CORS
import instaloader
import time
import random

app = Flask(__name__)
CORS(app)  # Allow Netlify / frontend requests

# Instaloader instance
L = instaloader.Instaloader()

# =========================
# Root test route
# =========================
@app.route("/", methods=["GET"])
def home():
    return "Backend is live ✅"

# =========================
# Download API
# =========================
@app.route("/download", methods=["POST"])
def download():
    data = request.get_json()

    if not data or "url" not in data:
        return jsonify({
            "status": "error",
            "message": "URL is required"
        }), 400

    url = data.get("url")

    if "instagram.com" not in url:
        return jsonify({
            "status": "error",
            "message": "Invalid Instagram URL"
        }), 400

    try:
        # Human-like delay (avoid instant blocking)
        time.sleep(random.uniform(2, 4))

        # Extract shortcode
        shortcode = url.strip("/").split("/")[-1]

        # Fetch post
        post = instaloader.Post.from_shortcode(L.context, shortcode)

        # Return video URL
        return jsonify({
            "status": "success",
            "video_url": post.video_url
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Unable to download video"
        }), 500


# =========================
# Run app (Render)
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
