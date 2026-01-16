from flask import Flask, request, jsonify
from flask_cors import CORS
import instaloader
import time, random

app = Flask(__name__)
CORS(app)  # allow Netlify requests

L = instaloader.Instaloader()

@app.route("/download", methods=["POST"])
def download():
    data = request.get_json()
    url = data.get("url")

    if not url or "instagram.com" not in url:
        return jsonify({"error": "Invalid URL"}), 400

    try:
        # human-like delay
        time.sleep(random.uniform(2, 4))

        shortcode = url.strip("/").split("/")[-1]
        post = instaloader.Post.from_shortcode(L.context, shortcode)

        return jsonify({
            "status": "success",
            "video_url": post.video_url
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Unable to download video"
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
