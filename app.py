from flask import Flask, render_template, request, jsonify, Response
import os
import yt_dlp
import time
import threading

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Global variable to store download progress
progress_data = {
    'percent': 0
}

# Progress hook function for yt-dlp
def progress_hook(d):
    if d['status'] == 'downloading':
        progress_data['percent'] = d.get('percent', 0)
    elif d['status'] == 'finished':
        progress_data['percent'] = 100

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_playlist():
    playlist_url = request.form['playlist_url']
    download_dir = os.path.expanduser('~') + '/Downloads'  # Default to Downloads folder

    # Set download options
    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
        'progress_hooks': [progress_hook],  # Register the progress hook
    }

    # Start a separate thread to handle the download without blocking the main server thread
    def download():
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([playlist_url])

    # Run the download in a background thread
    thread = threading.Thread(target=download)
    thread.start()

    return jsonify(success=True)

# Route to stream progress data to the frontend
@app.route('/progress')
def get_progress():
    def generate():
        while progress_data['percent'] < 100:
            yield f"data: {progress_data['percent']}\n\n"
            time.sleep(1)
        yield f"data: {progress_data['percent']}\n\n"
    
    return Response(generate(), content_type='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True)
