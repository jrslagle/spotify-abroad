import os
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
import re
from models import DB, AudioFeatures


load_dotenv()


global SPOTIPY_CLIENT_ID
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
global SPOTIPY_CLIENT_SECRET
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())


def get_audio_features(uri):
    """Posts audio features to the database
    :param uri: uri
    :return: -
    """
    try:
        uri = str(uri)
        res = re.findall(r':(?: *([\w.-]+):)', uri)
        str_res = ' '.join([str(word) for word in res])

        if str_res in ['playlist', 'userplaylist']:
            # from the playlist get URIs for each artist
            artist_uris_total = get_artists_from(uri)
            # from artist uris get a list of album uris
            albums_uris_total = []
            for artist_uri in artist_uris_total:
                album_uris = get_albums_from(artist_uri)
                albums_uris_total.extend(album_uris)
            # from a list of albums get tracks
            track_uris_total = []
            for albums_uri in albums_uris_total:
                tracks_uris = get_tracks_from(albums_uri)
                track_uris_total.extend(tracks_uris)
            print(track_uris_total)
            for track_uri in track_uris_total:
                features_to_db(track_uri)

        elif str_res == 'artist':
            albums_uris_total = get_albums_from(uri)
            track_uris_total = []
            for albums_uri in albums_uris_total:
                tracks_uris = get_tracks_from(albums_uri)
                track_uris_total.extend(tracks_uris)
            print(track_uris_total)
            for track_uri in track_uris_total:
                features_to_db(track_uri)

        elif str_res == 'album':
            track_uris_total = get_tracks_from(uri)
            print(track_uris_total)
            for track_uri in track_uris_total:
                features_to_db(track_uri)

        elif str_res == 'track':
            features_to_db(uri)

    except Exception as e:
        print("Error processing {}: {}".format(uri, e))
        raise e

    else:
        DB.session.commit()


def features_from_category(cat_id):
    """Posts tracks from the
    category to the database
    :param cat_id: category id
    :return:
    """

    try:
        playlists_uris = get_playlists_from(cat_id)
        artist_uris_total = []
        for playlist_uri in playlists_uris:
            artist_uris = get_artists_from(playlist_uri)
            artist_uris_total.append(artist for artist in artist_uris)
        albums_uris_total = []
        for artist_uri in artist_uris_total:
            album_uris = get_albums_from(artist_uri)
            albums_uris_total.append(album for album in album_uris)
        # from a list of albums get tracks
        track_uris_total = []
        for albums_uri in albums_uris_total:
            tracks_uris = get_tracks_from(albums_uri)
            track_uris_total.append(track for track in tracks_uris)
        for track_uri in track_uris_total:
            features_to_db(track_uri)

    except Exception as e:
        print("Error processing {}: {}".format(cat_id, e))
        raise e

    else:
        DB.session.commit()


def get_playlists_from(category_id):
    """Using Spotify API gets playlists' URIs from a category

    :param playlist_uri: URI
    :return: list of playlists' URIs from a category
    """
    playlist_uris = []
    for item in spotify.category_playlists(category_id)['playlists']['items']:
        playlist_uris.append(item['uri'])

    return playlist_uris


def get_artists_from(playlist_uri):
    """Using Spotify API gets artists' URIs from a playlist

    :param playlist_uri: URI
    :return: list of artists' URIs from a playlist
    """
    artist_uris = []
    playlist = spotify.playlist_items(playlist_uri)['items'][0]
    for artist in playlist['track']['album']['artists']:
        artist_uris.append(artist['uri'])

    return artist_uris


def get_albums_from(artist_uri):
    """Using Spotify API gets albums' URIs from an artist

    :param artist_uri: URI
    :return: list of albums' URIs from some artist
    """
    album_uris = []
    results = spotify.artist_albums(artist_uri, album_type='album')
    albums = results['items']
    # get URIs for each album
    for album in albums:
        album_uris.append(album['uri'])

    return album_uris


def get_tracks_from(album_uri):
    """Using Spotify API gets tracks' URIs from album

    :param album_uri: URI
    :return: list of track URIs from an album
    """
    track_uris = []
    album = spotify.album_tracks(album_id=album_uri)

    for track in album['items']:
        track_uris.append(track['uri'])

    return track_uris


def features_to_db(track_uri):
    """
    Adds audio features to the db
    :param track_uri: uri
    :return:
    """
    data = spotify.audio_features(track_uri)[0]
    audio_features = AudioFeatures(**data)
    DB.session.add(audio_features)
    # id, uri, danceability, energy, key, loudness, mode,
    # speechiness, acousticness, instrumentalness,
    # liveness, valence, tempo, type
