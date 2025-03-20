DATABASE_ID = "161ca7df301d803e9f6ee9714e90712e"
INVENTORY_ID = "16fca7df301d8019a4a1e699e85fa1eb"
NOTION_TOKEN = "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"

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

_data_file = "data"

import shelve, os
def _get_username():
    with shelve.open(_data_file) as db:
        if "username" not in db:
            db["username"] = os.getlogin()
        return db["username"]
def set_username(username):
    with shelve.open(_data_file) as db:
        db["username"] = username

USERNAME = _get_username()

def USERNAME(new=None):
    if new: set_username(new)
    return _get_username()