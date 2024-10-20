import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

CLIENT_ID = "fe5f03219c5a4491a22fabc1a154758cpip"
CLIENT_SECRET = "437a6815460c4d7bb676f72d421f789b"

# Initialize the Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        print(album_cover_url)
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"

def recommend(song):
    index = music[music['song'] == song].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_music_names = []
    recommended_music_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        artist = music.iloc[i[0]].artist
        print(artist)
        print(music.iloc[i[0]].song)
        recommended_music_posters.append(get_song_album_cover_url(music.iloc[i[0]].song, artist))
        recommended_music_names.append(music.iloc[i[0]].song)

    return recommended_music_names,recommended_music_posters

st.header('Music Recommender System')
music = pickle.load(open('df.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

df = pd.DataFrame({
    'song_name': ['Song1', 'Song2', 'Song3'],
    'artist': ['Artist1', 'Artist2', 'Artist3']
})

# Save the DataFrame to a pickle file
with open('df.pkl', 'wb') as f:
    pickle.dump(df, f)

# Example similarity matrix (replace this with your actual similarity data)
similarity = [[1, 0.9, 0.2], [0.9, 1, 0.3], [0.2, 0.3, 1]]

# Save the similarity matrix to a pickle file
with open('similarity.pkl', 'wb') as f:
    pickle.dump(similarity, f)

music_list = music['song'].values
selected_movie = st.selectbox(
    "Type or select a song from the dropdown",
    music_list
)

if st.button('Show Recommendation'):
    recommended_music_names,recommended_music_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5= st.columns(5)
    with col1:
        st.text(recommended_music_names[0])
        st.image(recommended_music_posters[0])
    with col2:
        st.text(recommended_music_names[1])
        st.image(recommended_music_posters[1])

    with col3:
        st.text(recommended_music_names[2])
        st.image(recommended_music_posters[2])
    with col4:
        st.text(recommended_music_names[3])
        st.image(recommended_music_posters[3])
    with col5:
        st.text(recommended_music_names[4])
        st.image(recommended_music_posters[4])



