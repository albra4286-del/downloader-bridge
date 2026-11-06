from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return "Bridge is active and running!"

@app.route('/download', methods=['GET'])
def download():
    target_url = request.args.get('url')
    if not target_url:
        return "Error: No URL provided", 400

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(target_url, headers=headers, stream=True, timeout=30)

        return Response(
            response.iter_content(chunk_size=8192),
            status=response.status_code,
            content_type=response.headers.get('content-type', 'application/octet-stream')
        )
    except Exception as e:
        return f"Error connecting to target: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
