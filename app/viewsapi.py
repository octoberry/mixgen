# coding=utf-8
from flask import request, jsonify
from pony.orm import db_session
from app import smart_pg
from app.server import app


@app.route('/api/find_tracks/<title>')
@db_session
def find_tracks(title):
    tracks = smart_pg.find_tracks(title)
    return jsonify({'tracks': tracks})


@app.route('/api/generate_playlist/<track_id>')
@db_session
def generate_playlist(track_id):
    plist = smart_pg.generate_playlist(track_id)
    return jsonify({'playlist': plist})

