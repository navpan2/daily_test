from flask import Flask, request, jsonify

import yt_dlp

app = Flask(__name__)

@app.route("/")
def root():
    return jsonify({"message": "Hello World"})

@app.route("/dailymo/")
def read_item():
    req_url = request.args.get('reqUrl', 'https://www.dailymotion.com/video/x8pdo3p')
    vid_format = request.args.get('vidFormat', 'http-720-0')

    video_url = req_url
    desired_format = vid_format

    ydl_opts = {
        'quiet': True,
        'format': desired_format,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=False)
        format_url = info_dict.get('url')

    if format_url:
        return jsonify({"url": format_url, "reqUrl": req_url, "vidFormat": vid_format})
    else:
        return jsonify({"url": "Not found", "reqUrl": req_url, "vidFormat": vid_format})

if __name__ == "__main__":
    app.run(debug=True)
