from flask import Flask, render_template, request, send_file, jsonify
from pytube import YouTube
import os

app = Flask(__name__)
app.config['TIMEOUT'] = 60

@app.route('/data')
def get_data():
    data = {
        'name': 'John Doe',
        'age': 30,
        'is_admin': True,
    }
    return jsonify(data)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def download():
    url = request.form['url']
    yt = YouTube(url, on_progress_callback=progress_function)
    audio_stream = yt.streams.filter(only_audio=True).first()
    output_file_path = "my_song.mp3"
    audio_stream.download(output_path=".", filename=output_file_path)
    return send_file(output_file_path, as_attachment=True)

@app.route('/progress')
def progress():
    if 'progress' in globals():
        return jsonify(progress=progress)
    else:
        return jsonify(progress=0)

def progress_function(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = bytes_downloaded / total_size * 100
    kb_downloaded = bytes_downloaded / 1024
    global progress
    progress = {'percentage': percentage, 'kb_downloaded': kb_downloaded}

if __name__ == '__main__':
    app.run(debug=True)
