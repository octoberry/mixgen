# -*- coding: utf-8 -*-
__author__ = 'fuse'

from server import app
from pymongo import MongoClient

client = MongoClient(app.config['MONGODB_CONNECT'])

db = client.mixcloud

def to_list(x):
    return [x] if not isinstance(x, list) else x

def find_tracks(search, limit=20, exclude_remixes=False):
    terms = search.split()
    search = ' '.join(['%s' % x for x in to_list(terms)])
    if exclude_remixes:
        search += ' -remix'
    songs = db.all_songs.find(
        {'$text': {'$search': search}},
        {'score': {'$meta': 'textScore'}}
    ).sort([('score', {'$meta': 'textScore'})])

    items = []
    for s in songs:
        t = db.music_track.find_one({'artist_id': s['artist_id'], 'song_id': s['song_id']})
        if t:
            cnt = db.music_section.find({'track_id': t['id']}).count()
            if cnt:
                items.append({'track_id': t['id'], 'title': '%s - %s' % (s['artist'], s['song']), 'count': cnt})
                if len(items) >= limit:
                    break

    return sorted(items, key=lambda x: x['count'], reverse=True)

def generate_playlist(track_id, limit=20):
    sections = db.music_section.find({'track_id': track_id})
    cloudcast_ids = [s['cloudcast_id'] for s in sections]
    res = db.music_section.aggregate([
        {'$match': {'cloudcast_id': {'$in': cloudcast_ids}}},
        {'$group': {'_id': '$track_id', 'cnt': {'$sum': 1}, 'pos': {'$avg': '$position'}}},
        {'$sort': {'cnt': -1, 'pos': 1}}
    ])

    plist = []
    for x in res['result'][:limit]:
        t = db.music_track.find_one({'id': x['_id']})
        s = db.all_songs.find_one({'artist_id': t['artist_id'], 'song_id': t['song_id']})
        if s:
            plist.append({'title': '%s - %s' % (s['artist'], s['song']), 'count': x['cnt'], 'position': x['pos']})

    return plist


if __name__ == "__main__":
    songs = find_tracks("Kevin Rudolf In the city")
    plist = generate_playlist(songs[0]['track_id'])
    for x in plist:
        print x

