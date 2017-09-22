import pprint
import sys

import spotipy
import spotipy.util as util


def get_top_tracks( sp, limit = 50 ):
   r = 'long_term'
   results = sp.current_user_top_tracks(time_range=r, limit=50)
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
    playlist_id = '7sJlGU5BLOXA5R5b8IqKrm'

    # GET CURRENT TOP TRACKS
    items = get_top_tracks(sp, 50)
    tracks = []
    for i in items:
        tracks.append(i['uri'].replace('spotify:track:', ''))

    sp.user_playlist_replace_tracks(username, playlist_id, tracks )
else:
    print ("Can't get token for " + username)
