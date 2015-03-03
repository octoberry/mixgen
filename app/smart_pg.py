# coding=utf-8
from app.server import db


def find_tracks(search, limit=20, exclude_remixes=False):
    terms = search.split()
    if exclude_remixes:
        terms.append('!remix')
    tsquery = ' & '.join(terms)
    res = db.select(
        "select s.artist_id, s.song_id, s.title, count(ms.id) as cnt "
        "from (select artist_id, song_id, title, ts_rank_cd(title_ts, query, 8) as rank "
            "from all_songs, to_tsquery($tsquery) query "
            "where title_ts @@ query order by rank desc limit $limit) s "
        "join music_track t using (artist_id, song_id) "
        "join music_section ms on ms.track_id = t.id "
        "group by s.artist_id, s.song_id, s.title order by cnt desc"
    )
    tracks = []
    for row in res:
        tracks.append({
            'track_id': '%s:%s' % (row.artist_id, row.song_id),
            'title': row.title,
            'count': row.cnt
        })
    return tracks


def generate_playlist(track_id, length=20):
    artist_id, song_id = track_id.split(':')
    res = db.select(
        "select s.title, p.cnt, p.pos "
        "from (select track_id, count(id) as cnt, avg(position) as pos from music_section "
            "join (select cloudcast_id from music_track mt join music_section ms on ms.track_id = mt.id "
                "where mt.artist_id = $artist_id and mt.song_id = $song_id) clouds using (cloudcast_id) "
            "group by track_id order by cnt desc, pos asc limit $length) p "
        "join music_track mt on mt.id = p.track_id join all_songs s using (artist_id, song_id)"
    )
    plist = []
    for row in res:
        plist.append({
            'title': row.title,
            'count': row.cnt,
            'position': float(row.pos)
        })
    return plist

