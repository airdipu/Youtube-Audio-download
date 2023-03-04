from flask import Flask, request, render_template, jsonify
from youtube_dl import YoutubeDL

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'progress_hooks': [progress_hook],
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return jsonify({'result': 'success'})
    return render_template('index.html')

@app.route('/progress')
def progress():
    return jsonify({'progress': {'percentage': percentage, 'kb_downloaded': kb_downloaded}})

@app.route('/status')
def status():
    return render_template('status.html')

def progress_hook(progress):
    global percentage, kb_downloaded
    if progress['status'] == 'downloading':
        total_bytes = progress.get('total_bytes')
        downloaded_bytes = progress.get('downloaded_bytes')
        if total_bytes and downloaded_bytes:
            percentage = downloaded_bytes / total_bytes * 100
            kb_downloaded = downloaded_bytes / 1024
    elif progress['status'] == 'finished':
        percentage = 100

if __name__ == '__main__':
    app.run()
