# -*- coding: utf-8 -*-
__author__ = 'fuse'

from server import app
from pymongo import MongoClient

client = MongoClient(app.config['MONGODB_CONNECT'])

db = client.mixcloud

def to_list(x):
    return [x] if not isinstance(x, list) else x

def find_song(terms):
    search = ' '.join(['"%s"' % x for x in to_list(terms)]) + ' -mix'
    return db.all_songs.find(
        {'$text': {'$search': search}},
        {'score': {'$meta': 'textScore'}}
    ).sort([('score', {'$meta': 'textScore'})])

def generate_playlist(search, limit=20):
    terms = search.split()
    songs = find_song(terms)
    items = []
    for s in songs:
        t = db.music_track.find_one({'artist_id': s['artist_id'], 'song_id': s['song_id']})
        if t:
            cnt = db.music_section.find({'track_id': t['id']}).count()
            if cnt:
                items.append({'song': s, 'track': t, 'sections': cnt})

    items = sorted(items, key=lambda x: x['sections'], reverse=True)
    track = items[0]['track']
    sections = db.music_section.find({'track_id': track['id']})
    cloudcast_ids = [s['cloudcast_id'] for s in sections]
    res = db.music_section.aggregate([
        {'$match': {'cloudcast_id': {'$in': cloudcast_ids}}},
        {'$group': {'_id': '$track_id', 'cnt': {'$sum': 1}}},
        {'$sort': {'cnt': -1}}
    ])
    plist = []
    for x in res['result'][:limit]:
        t = db.music_track.find_one({'id': x['_id']})
        s = db.all_songs.find_one({'artist_id': t['artist_id'], 'song_id': t['song_id']})
        if s:
            # print s['artist'], s['song'], x['cnt']
            plist.append('%s %s' % (s['artist'], s['song']))

    return plist


if __name__ == "__main__":
    plist = generate_playlist("Elliphant revolusion")
    print "\n".join(plist)

