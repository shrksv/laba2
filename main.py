"""
Lab_2, Task_2
"""
import os
import json
import base64
import requests
from dotenv import load_dotenv

load_dotenv()
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')


def get_token() -> str:
    """
    The function return token
    :return: something
    """
    auth_string = client_id + ':' + client_secret
    auth_bytes = auth_string.encode('utf-8')
    auth_bases64 = str(base64.b64encode(auth_bytes), "utf-8")
    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic ' + auth_bases64,
        'Content-type': 'application/x-www-form-urlencoded'
    }
    data = {'grant_type': "client_credentials"}
    result = requests.post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token


token = get_token()


def get_auth_header(token):
    return {'Authorization': 'Bearer ' + token}

def search_for_artist(token, artist_name):
    """
    """
    url = 'https://api.spotify.com/v1/search'
    headers = get_auth_header(token)
    query = f'?q={artist_name}&type=artist&limit=1'

    query_url = url + query
    result = requests.get(query_url, headers=headers)
    json_result = json.loads(result.content)['artists']['items']
    json_result2 = json.loads(result.content)
    if len(json_result) == 0:
        print('No artist found')
        return None
    return json_result[0], json_result2

def get_songs_by_artist(token, artist_id: str):
    url = f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=us'
    headers = get_auth_header(token)
    result = requests.get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    f = open('json_result.json', 'w')
    json.dump(json_result, f, indent=4, ensure_ascii = False)
    return json_result

def available_markers(token, songid):
    url = f"https://api.spotify.com/v1/tracks/{songid}"
    headers = get_auth_header(token)
    result = requests.get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result.get("available_markets", [])

# token = get_token()
# result = search_for_artist(token, 'ACDC')


def main():
    print("Enter artist name:")
    artist_name = input(">>> ")
    token = get_token()
    result, info = search_for_artist(token, artist_name)
    artist_id = result["id"]
    songs = get_songs_by_artist(token, artist_id)
    avaliable_marker = available_markers(token, songs[0]['id'])
    print("What do you want to know about that artist:\n\
          1. Famous song\n\
          2. Artist ID\n\
          3. Original name\n\
          4. Genre\n\
          5. Markers")
    num = input(">>> ")
    if num.isdigit():
        if num in ['1','2','3','4', '5']:
            if num == "1":
                print(f"Their famous song is : '{songs[0]['name']}'")
                return None
            if num == "2":
                print(f"Artist id is: {artist_id}")
                return None
            if num == "3":
                print(f"Original name: {songs[0]['album']['artists'][0]['name']}")
                return None
            if num == "4":
                print(f"Genres: {result['genres']}")
                return None
            if num == "5":
                print(f"Markers: {avaliable_marker}")
                return None
    print("Incorrect number")
    return None

main()
