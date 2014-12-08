# coding=utf-8
import json
from flask import render_template, request
from app import smart
from app.server import app
from app.youtube import youtube_search


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/new', methods=['POST', 'GET'])
def new():
    track_title = request.form['title']
    tracks = smart.find_tracks(track_title)
    return render_template('new.html', tracks=tracks)


@app.route('/player', methods=['POST'])
def player():
    track_title = request.form['title']
    track_id = request.form['track_id']
    videos = youtube_search(query=track_title, max_results=1)
    if videos:
        videos[0]['yt_id'] = videos[0]['id']
        videos[0]['track_id'] = track_id
        return json.dumps(videos[0])

@app.route('/playlist', methods=['POST'])
def playlist():
    track_id = int(request.form['track_id'])
    length = int(request.form['length'])
    plist = smart.generate_playlist(track_id, length)
    for item in plist:
        videos = youtube_search(query=item['title'], max_results=1)
        if videos:
            item['yt_id'] = videos[0]['id']
    return render_template('playlist.html', playlist=plist, yt_ids=[t['yt_id'] for t in plist if t.get('yt_id')])
