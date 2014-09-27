# coding=utf-8
import json
from flask import render_template, request
from app.server import app
from app.youtube import youtube_search


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/new', methods=['POST', 'GET'])
def new():
    tracks = [
        {'id': 6, 'title': 'Disclosure - Voices ft. Sasha Keable'},
        {'id': 7, 'title': 'Moby'},
    ]
    return render_template('new.html', tracks=tracks)


@app.route('/player', methods=['POST'])
def player():
    track_title = request.form['title']
    track_id = request.form['id']
    videos = youtube_search(query=track_title, max_results=1)
    if videos:
        videos[0]['track_id'] = track_id
        return json.dumps(videos[0])

@app.route('/playlist', methods=['POST'])
def playlist():
    playlist = [
        {'title': 'Moby'},
        {'title': 'Moby'},
        {'title': 'Moby'},
        {'title': 'Moby'},
    ]
    for item in playlist:
        videos = youtube_search(query=item['title'], max_results=1)
        if videos:
            item['yt_id'] = videos[0]['id']
    return render_template('playlist.html', playlist=playlist)
