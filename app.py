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
    yt = YouTube(url, on_progress_callback=progress_function)
    audio_stream = yt.streams.filter(only_audio=True).first()
    output_file_path = "my_song.mp3"
    audio_stream.download(output_path=".", filename=output_file_path)
    return send_file(output_file_path, as_attachment=True)

def progress_function(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = bytes_downloaded / total_size * 100
    kb_downloaded = bytes_downloaded / 1024
    print(f"Downloaded {kb_downloaded:.2f} KB ({percentage:.2f}%) of {total_size / 1024 / 1024:.2f} MB")
    # send progress information to client using WebSocket
    socketio.emit('progress', {'percentage': percentage, 'kb_downloaded': kb_downloaded})

if __name__ == '__main__':
    # set up Flask-SocketIO
    from flask_socketio import SocketIO, emit
    app.config['SECRET_KEY'] = 'secret!'
    socketio = SocketIO(app)

    @app.route('/progress')
    def progress():
        return render_template('progress.html')

    # handle WebSocket connections from client
    @socketio.on('connect')
    def test_connect():
        print('Client connected')

    @socketio.on('disconnect')
    def test_disconnect():
        print('Client disconnected')

    socketio.run(app, debug=True)
