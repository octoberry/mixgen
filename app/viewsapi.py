# coding=utf-8
from flask import request, jsonify, url_for
from pony.orm import db_session
from app import smart_pg
from app.server import app


@app.route('/api/find_tracks/<string:title>')
@db_session
def find_tracks(title):
    tracks = smart_pg.find_tracks(title)
    plist_url = lambda tid: url_for('generate_playlist', track_id=tid, _external=True)
    tracks = [dict(x, plist_url=plist_url(x['track_id'])) for x in tracks]
    return jsonify({'tracks': tracks})


@app.route('/api/generate_playlist/<string:track_id>')
@db_session
def generate_playlist(track_id):
    plist = smart_pg.generate_playlist(track_id)
    return jsonify({'playlist': plist})

