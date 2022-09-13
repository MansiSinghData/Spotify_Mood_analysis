# importing required libraries

import pandas as pd
import requests
import datetime
from conxn import coxn

USER_ID=" "

# token for recently played songs
playlist_token=' '

# audio features of the recently played songs
features_token = ' '

# Base URL for extracting audio features of recently played songs
BASE_URL = 'https://api.spotify.com/v1/'

if __name__=="__main__":
    # declaring headers
    playlist_headers={"Accept":"Application/json",
             "Content-type":"Application/json",
             "Authorization":"Bearer {token}".format(token=playlist_token)
             }

    audio_features_headers = {"Accept": "Application/json",
               "Content-type": "Application/json",
               "Authorization": "Bearer {token}".format(token=features_token)
               }
    # calculating time for last 24 hours to get songs played in last 24 hours and converting to unix time format
    today=datetime.datetime.now()
    yesterday=today-datetime.timedelta(days=1)
    yesterday_unix=int(yesterday.timestamp())*1000

    # Requesting data from api
    r=requests.get("https://api.spotify.com/v1/me/player/recently-played?after={time}".format(time=yesterday_unix), headers = playlist_headers)
    data = r.json()


    song_id= []
    song_names = []
    artist_names = []
    played_at_list = []
    song_uri =[]
    timestamps = []


    # Extracting only the relevant part of data from the json object
    for song in data["items"]:
        song_id.append(song["track"]["id"])
        song_names.append(song["track"]["name"])
        artist_names.append(song["track"]["album"]["artists"][0]["name"])
        played_at_list.append(song["played_at"])
        song_uri.append(song["track"]["uri"])
        timestamps.append(song["played_at"][0:10])

    # Preparing dictionary for converting to a dataframe
    song_dict = {
        "song_id":song_id,
        "song_name": song_names,
        "artist_name": artist_names,
        "played_at": played_at_list,
        "song_uri":song_uri,
        "timestamp": timestamps
    }

    song_df = pd.DataFrame(song_dict, columns=["song_id","song_name", "artist_name", "played_at","song_uri", "timestamp"])
    # print(song_df)

    # sending the data to SQLSERVER  Database
    song_df.to_sql('SONGS',con=coxn,schema='dbo',if_exists='append',index=True)

    feature_dict = {}
    # converting the song id list to values separated by %2C
    song_id_list='%2C'.join(song_id)
 

    s = requests.get(BASE_URL + 'audio-features?ids=' + song_id_list, headers=audio_features_headers)
    s = s.json()

    df_features = pd.DataFrame.from_dict(s['audio_features'])

    # sending audio features data to SQLSERVER Database
    df_features.to_sql('SONGS_FEATURES_DATA', con=coxn, schema='dbo', if_exists='append', index=True)






