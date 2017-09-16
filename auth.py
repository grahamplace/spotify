
import pprint
import sys
import os
import subprocess

import spotipy
import spotipy.util as util


client_id = c_id
client_secret = c_secret

# python -m SimpleHTTPServer 8888
redirect_uri = 'http://localhost:8888/callback/'

scope = 'user-library-read user-read-recently-played user-read-currently-playing user-modify-playback-state '
scope += 'user-read-playback-state user-top-read user-read-email user-read-birthdate user-read-private user-library-modify '
scope += 'user-library-read user-follow-read user-follow-modify ugc-image-upload streaming playlist-modify-private playlist-modify-public playlist-read-collaborative playlist-read-private'
if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print "Usage: %s username" % (sys.argv[0],)
    sys.exit()

token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)

if token:
    print 'Quick test that everything is working: '
    sp = spotipy.Spotify(auth=token)
    results = sp.current_user_saved_tracks()
    for item in results['items']:
        track = item['track']
        print track['name'] + ' - ' + track['artists'][0]['name']
else:
    print "Can't get token for", username
