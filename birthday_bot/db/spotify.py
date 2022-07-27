import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import database
import json

k_genre = ["k-rap", "korean r&b", "korean trap", "k-pop", "k-indie", "korean pop", "korean underground rap",
           "korean hyperpop"]


# 참조
# https://developer.spotify.com/documentation/web-api/reference/#/operations/search
def search_and_insert(q: str, offset: int, limit: int):
    fboard_rapper_list = []
    kboard_rapper_list = []

    with open('./../secret.json', encoding='UTF-8') as f:
        secret = json.load(f)

    client_credentials_manager = SpotifyClientCredentials(client_id=secret["spotify_id"], client_secret=secret["spotify_pw"])
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    artists = sp.search(q=q, type="artist", offset=offset, limit=limit)
    print(artists)
    for i in range(len(artists["artists"]["items"])):
        print("-"*50)
        print(artists["artists"]["items"][i]["name"], artists["artists"]["items"][i]["external_urls"]["spotify"])
        print(artists["artists"]["items"][i]["id"])
        print("popularity :", artists["artists"]["items"][i]["popularity"])
        print(artists["artists"]["items"][i]["genres"])

        k_bool = False

        # 국내래퍼는 kboard 테이블로
        for k in range(len(k_genre)):
            if k_genre[k] in artists["artists"]["items"][i]["genres"]:
                k_bool = True

        if k_bool:
            kboard_rapper_list.append({
                "spotify_id": artists["artists"]["items"][i]["id"],
                "name": artists["artists"]["items"][i]["name"],
                "birthday": None,
                "popularity": artists["artists"]["items"][i]["popularity"],
                "genres": str(artists["artists"]["items"][i]["genres"])
            })
        else:
            if int(artists["artists"]["items"][i]["popularity"]) > 30:
                fboard_rapper_list.append({
                    "spotify_id": artists["artists"]["items"][i]["id"],
                    "name": artists["artists"]["items"][i]["name"],
                    "birthday": None,
                    "popularity": artists["artists"]["items"][i]["popularity"],
                    "genres": str(artists["artists"]["items"][i]["genres"])
                })

    print("-"*50)
    print("불러온 아티스트 목록을 데이터 베이스에 업데이트 할까요?")
    ask = str(input("(y/n) : "))

    if ask == "Y" or ask == "y" or ask == "ㅛ":
        if len(kboard_rapper_list) > len(fboard_rapper_list):
            database.insert("kboard", kboard_rapper_list)
        else:
            database.insert("fboard", fboard_rapper_list)
            if len(kboard_rapper_list) > 0:
                database.insert("kboard",kboard_rapper_list)


if __name__ == '__main__':
    search_and_insert("아웃사이더", 0, 1)
