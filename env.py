VERSION = "v0.1.1"

import shelve, os


_data_file = "bancai_data"

def _get_username():
    with shelve.open(_data_file) as db:
        if "username" not in db:
            db["username"] = os.getlogin()
        return db["username"]
def _set_username(username):
    with shelve.open(_data_file) as db:
        db["username"] = username

#USERNAME = _get_username()

def USERNAME(new=None):
    if new: _set_username(new)
    return _get_username()



def _get_token():
    with shelve.open(_data_file) as db:
        if "NOTION_TOKEN" not in db:
            return None
        return db["NOTION_TOKEN"]
def _set_token(token):
    with shelve.open(_data_file) as db:
        db["NOTION_TOKEN"] = token

def HEADERS(token=None):
    if token: _set_token(token)
    token = _get_token()
    if token:
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
    else: return None

DATABASE_ID = "161ca7df301d803e9f6ee9714e90712e"
INVENTORY_ID = "16fca7df301d8019a4a1e699e85fa1eb"
