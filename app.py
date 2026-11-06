import os
import glob
from flask import Flask, request, send_file, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/download', methods=['GET'])
def download_media():
    url = request.args.get('url')
    file_type = request.args.get('type', 'video')
    is_check = request.args.get('check', 'false')

    if not url:
        return jsonify({"error": "No URL provided")), 400

    for old_file in glob.glob("downloaded_media.*"):
        try:
            os.remove(old_file)
        except:
            pass

    if is_check == 'true':
        try:
            ydl_opts = {'quiet': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.extract_info(url, download=False)
            return jsonify({"status": "success", "message": "URL is valid"})
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    try:
        if file_type == 'audio':
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': 'downloaded_media.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
        else:
            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'outtmpl': 'downloaded_media.%(ext)s',
            }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            if file_type == 'audio':
                base, _ = os.path.splitext(filename)
                filename = base + '.mp3'

        if os.path.exists(filename):
            return send_file(filename, as_attachment=True)
        else:
            return jsonify({"error": "Failed to generate media file"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
