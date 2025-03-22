from env import VERSION
import requests


def check_last_version():
    url = "https://api.github.com/repos/rir001/CAI_prestamos/releases/latest"
    response = requests.get(url)
    if response.status_code == 200 and response.json()["tag_name"] > VERSION:
        return response.json()["tag_name"]
    else:
        return None
