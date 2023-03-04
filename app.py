from flask import Flask, request, render_template, jsonify, redirect, url_for
from youtube_dl import YoutubeDL

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'audio.%(ext)s',
            'noplaylist': True,
            'progress_hooks': [progress_hook],
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return redirect(url_for('status'))
    return render_template('index.html')

@app.route('/progress')
def progress():
    return jsonify({'progress': progress_dict})

@app.route('/status')
def status():
    return render_template('status.html', kb_downloaded=progress_dict['kb_downloaded'], percentage=progress_dict['percentage'])

@app.route('/back')
def back():
    return redirect(url_for('index'))

def progress_hook(d):
    if d['status'] == 'finished':
        progress_dict['kb_downloaded'] = d.get('total_bytes', 0) / 1024
        progress_dict['percentage'] = 100.0
    elif d['status'] == 'downloading':
        if d.get('total_bytes'):
            kb_downloaded = d.get('downloaded_bytes', 0) / 1024
            total_size = d.get('total_bytes', 0) / 1024
            progress_dict['kb_downloaded'] = kb_downloaded
            progress_dict['percentage'] = (kb_downloaded / total_size) * 100

if __name__ == '__main__':
    progress_dict = {'kb_downloaded': 0, 'percentage': 0}
    app.run(debug=True)
