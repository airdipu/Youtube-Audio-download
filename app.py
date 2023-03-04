'''

To download youtube video as a audio, need to run this app

'''
from flask import Flask, render_template, request, send_file
from pytube import YouTube
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def download():
    url = request.form['url']
    yt = YouTube(url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    output_file_path = "my_song.mp3"
    audio_stream.download(output_path=".", filename=output_file_path)
    return send_file(output_file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)