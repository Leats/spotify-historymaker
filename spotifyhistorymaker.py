import configparser
import json
import psycopg2
import requests


def get_access_token(refresh_token: str) -> str:
    """Use the given refresh-token to get a new and valid access
    token. If successful the access token will be returned.
    """
    config = configparser.ConfigParser()
    config.read('config.ini')

    payload = {
        'refresh_token': config['Spotify']['Refreshtoken'],
        'grant_type': 'refresh_token',
    }

    r = requests.post(
        'https://accounts.spotify.com/api/token',
        data=payload,
        auth=(config['Spotify']['Clientid'], config['Spotify']['Clientsecret']),
    )

    r.raise_for_status()
    return r.json()['access_token']


def get_recent_tracks(access_token: str) -> str:
    """Use the access token to connect to Spotify
    and get the most recent played tracks
    (up to 50, as set by Spotify's API).
    """
    bearer_token = f'Bearer {access_token}'

    track_headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': bearer_token,
    }

    track_params = (('type', 'track'), ('limit', '50'))

    response = requests.get(
        'https://api.spotify.com/v1/me/player/recently-played',
        headers=track_headers,
        params=track_params,
    )

    response.raise_for_status()
    return response


def get_artist_genres(access_token: str, artist_id: str):
    """Use Spotify's artist ID to get a list of genres
    in stringform. The genres are not returned when using
    get_recent_tracks(), which is why a different request
    is necessary.
    """
    bearer_token = f'Bearer {access_token}'

    track_headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': bearer_token,
    }

    response = requests.get(
        'https://api.spotify.com/v1/artists/' + artist_id, headers=track_headers
    )

    response.raise_for_status()

    return response.json()['genres']


def connect_to_database(connection: str) -> psycopg2.extensions.connection:
    """Establish connection to a database."""
    return psycopg2.connect(connection)


def insert_cursors(conn, after, before):
    """Insert Spotify's cursors into the database.
    Spotify uses Unix timestamps for their cursors.
    """
    cur = conn.cursor()

    cur.execute(
        '''INSERT INTO cursors (after,before) 
      VALUES (%s,%s)
      ON CONFLICT (after)
      DO NOTHING;''',
        (after, before),
    )


def insert_context(conn, uri, ctype):
    """Insert the context into the database.
    Spotify uses the context to note in which
    context the track was played. Can be null.
    """
    cur = conn.cursor()

    cur.execute(
        '''INSERT INTO context (uri,type) 
      VALUES (%s,%s)
      ON CONFLICT (uri)
      DO NOTHING;''',
        (uri, ctype),
    )


def insert_played(conn, trackuri, artisturi, time, contexturi=None):
    """Insert information about the actual playing of a song
    to the database. This is to give some kind of context to
    the played tracks. This version will be used when the context
    to the song played is not null.
    """
    cur = conn.cursor()

    cur.execute(
        '''INSERT INTO played (trackuri,artisturi,contexturi,time) 
      VALUES (%s, %s, %s, %s)
      ON CONFLICT (time)
      DO NOTHING;''',
        (trackuri, artisturi, contexturi, time),
    )


def insert_track(
    conn,
    title,
    uri,
    artisturi,
    albumuri,
    tid,
    duration,
    explicit,
    popularity,
    tracknumber,
):
    """Insert information about a specific track into the database.
    Will not write to database if the id of the song is already in the
    database.
    """
    cur = conn.cursor()

    cur.execute(
        '''INSERT INTO track (title,uri,artisturi,albumuri,id,duration,explicit,popularity,tracknumber) 
      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
      ON CONFLICT (id)
      DO NOTHING;''',
        (
            title,
            uri,
            artisturi,
            albumuri,
            tid,
            duration,
            explicit,
            popularity,
            tracknumber,
        ),
    )


def insert_album(conn, title, uri, artisturi, aid):
    """Insert information about an album to the database.

    Arguments:
        title {str} -- Title of the album
        uri {str} -- Spotify's URI of the album
        artisturi {str} -- Spotify URI of the artist
        aid {str} -- Spotify's unique album ID
    """
    cur = conn.cursor()

    cur.execute(
        '''INSERT INTO album (title,uri,artisturi,id) 
      VALUES (%s, %s, %s, %s)
      ON CONFLICT (id)
      DO NOTHING;''',
        (title, uri, artisturi, aid),
    )


def insert_artist(conn, name, uri, aid, gen):
    """Insert information about an artist to the database.

    Arguments:
        name {str} -- Name of artist
        uri {str} -- URI of the artist
        aid {str} -- Spotify's Artist ID
        gen {str} -- Genres of the artist. Preferably generated with get_artist_genres().
    """
    cur = conn.cursor()

    cur.execute(
        '''INSERT INTO artist (name,uri,id,genre) 
      VALUES (%s, %s, %s, %s)
      ON CONFLICT (id)
      DO NOTHING;''',
        (name, uri, aid, gen),
    )


def is_new_artist(conn, aid) -> bool:
    """Check if a specific artist ID is already in the database."""
    cur = conn.cursor()
    cur.execute("SELECT id FROM artist WHERE id=%s", (aid,))
    return cur.rowcount == 0


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    if len(config) == 0:
        raise ValueError("No valid config.ini available.")

    # The refresh token for Spotify.
    # For more information check: https://developer.spotify.com/documentation/general/guides/authorization-guide/
    refresh_token = config['Spotify']['Refreshtoken']

    # Generate a new access token with the refresh token:
    try:
        access_token = get_access_token(refresh_token)
    except requests.exceptions.HTTPError as err:
        print("Could not get refresh token from Spotify:")
        print(err)
        print("Exiting...")
        exit()
    access_token = get_access_token(refresh_token)

    # The actual request to spotify:
    try:
        response = get_recent_tracks(access_token)
    except requests.exceptions.HTTPError as err:
        print("Could not get recent tracks from Spotify:")
        print(err)
        print("Exiting...")
        exit()

    rjson = response.json()

    # Connection to the database according to config file:
    try:
        conn = connect_to_database(
            ' '.join('='.join(sub) for sub in config.items("Database"))
        )
    except psycopg2.Error as err:
        print(err)
        print("Exiting...")
        exit()

    # Cursors are inserted into the database:
    insert_cursors(conn, rjson['cursors']['after'], rjson['cursors']['before'])

    for item in rjson['items']:
        track = item['track']
        album = item['track']['album']
        # Note: Only the main artist will get saved to the database:
        artist = item['track']['artists'][0]

        # Album information is inserted into the database:
        insert_album(conn, album['name'], album['uri'], artist['uri'], album['id'])
        # Track infromation is inserted into the database:
        insert_track(
            conn,
            track['name'],
            track['uri'],
            artist['uri'],
            album['uri'],
            track['id'],
            track['duration_ms'],
            track['explicit'],
            track['popularity'],
            track['track_number'],
        )

        # Check if the artist is not yet in the database.
        # This will prevent an unneccessary request to spotify to get the artist genres.
        if is_new_artist(conn, artist['id']):
            # Try to collect genres of new artist. If not possible, the artist will be added
            # without any genres.
            try:
                artist_genres = get_artist_genres(access_token, artist['id'])
            except requests.exceptions.HTTPError as err:
                print("Could not retrieve Artist Genres from Spotify:")
                print(err)
                print(f"Artist Genres of {artist['name']} will be left blank.")
                artist_genres = None

            insert_artist(
                conn, artist['name'], artist['uri'], artist['id'], artist_genres
            )

        if item['context'] is not None:
            insert_context(conn, item['context']['uri'], item['context']['type'])
            insert_played(
                conn,
                track['uri'],
                artist['uri'],
                item['played_at'],
                item['context']['uri'],
            )
        else:
            insert_played(conn, track['uri'], artist['uri'], item['played_at'])
        conn.commit()

    conn.close()


if __name__ == '__main__':
    main()
