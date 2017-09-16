import pprint
import sys

import spotipy
import spotipy.util as util


def get_recent_items( sp, limit = 50 ):
   results = sp._get("me/player/recently-played", limit=limit)
   items = results['items']
   return items

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print ("Usage: %s username playlist_id track_id ..." % (sys.argv[0],))
    sys.exit()

scope = 'playlist-modify-public'
token = util.prompt_for_user_token(username, scope)

if token:
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    playlist_id = '4XW1C9qdMjf0xbEsL1r7Zy'

    # GET RECENT PLAYS
    items = get_recent_items(sp, 50)
    albums = []
    tracks = []
    future = {}
    for i in items:
        track = i['track']
        album_uri = track['album']['uri']
        if album_uri not in albums:
            albums.append(album_uri)
            tracks.append(track['uri'].replace('spotify:track:', ''))
            future[ album_uri ] = track['uri'].replace('spotify:track:', '')

    # GET CURRENT PLAYLIST
    results = sp.user_playlist(username, playlist_id)
    current_items = results['tracks']['items']
    total_current = results['tracks']['total']

    current = {}
    for i in current_items:
        track = i['track']
        album_uri = track['album']['uri']
        current[ album_uri ] = track['uri'].replace('spotify:track:', '')

    # UPDATE FINAL PLAYLIST OF 100, DONT ADD DUPLICATE ALBUMS
    final_tracks = tracks
    final_albums = albums
    for a, t in current.iteritems():
        if a not in final_albums:
            final_albums.append(a)
            final_tracks.append(t)
        if len(final_tracks) >= 100:
            break

    sp.user_playlist_replace_tracks(username, playlist_id, final_tracks )
else:
    print ("Can't get token for " + username)
