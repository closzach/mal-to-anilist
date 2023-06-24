import requests
from configparser import ConfigParser

config  = ConfigParser()
config.read(r"config\config.ini")

_MAL_API_URL_ = config.get("mal", "mal_api_url")
CLIENT_ID = config.get("mal", "client_id")

headers = {
    "X-MAL-CLIENT-ID": CLIENT_ID
}

def get_mal_animelist(username, user_list_url=None):
    if user_list_url is None:
        user_list_url = _MAL_API_URL_ + "/users/" + username + "/animelist"
    r = requests.get(user_list_url, headers=headers)
    if r.status_code != requests.codes.ok:
        print(r.raise_for_status())
    data = r.json()["data"]
    if "next" in r.json()["paging"].keys():
        data += get_mal_animelist(username, r.json()["paging"]["next"])
    return data

def get_mal_mangalist(username, user_list_url=None):
    if user_list_url is None:
        user_list_url = _MAL_API_URL_ + "/users/" + username + "/mangalist"
    r = requests.get(user_list_url, headers=headers)
    if r.status_code != requests.codes.ok:
        print(r.raise_for_status())
    data = r.json()["data"]
    if "next" in r.json()["paging"].keys():
        data += get_mal_mangalist(username, r.json()["paging"]["next"])
    return data

if __name__ == "__main__":
    # Afficher la liste des noms des animés de l'utilisateur Heicleurc
    for anime in get_mal_animelist("Heicleurc"):
        print(anime["node"]["title"])

    # Afficher la liste des noms des mangas de l'utilisateur Heicleurc
    for manga in get_mal_mangalist("Heicleurc"):
        print(manga["node"]["title"])