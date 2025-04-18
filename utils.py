from params import DAY_PRICE, MAX_PRICE
from env import DATABASE_ID, INVENTORY_ID, HEADERS, VERSION
import requests
from datetime import datetime, timedelta, datetime, timezone
fromisoformat = datetime.fromisoformat
now_time = lambda : datetime.now(timezone.utc)



def test_token(token:str):
    url = "https://api.notion.com/v1/users"
    headers = {
        'Authorization': f'Bearer {token}',
        'Notion-Version': '2022-06-28'
    }
    response = requests.get(url, headers=headers)
    return response.status_code == 200

def calculate_fee(start, end, type=""):
    diff = end - start
    if type == "None":
        pass
    else:
        days = diff.days-1
        for i in range(days):
            if (start + timedelta(i+1)).weekday() in [5, 6]:
                days -= 1
        return min(max(days, 0)*DAY_PRICE, MAX_PRICE)

def get_debt(person, now=now_time()):
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

    filter_params = {
        "filter": {
            "and": [
                {
                    "property": "Persona",
                    "rich_text": {
                        "contains": person[:-2]
                    },
                },
                {
                    "property": "Estado",
                    "formula": {
                        "string": {
                            "contains": "🟠"
                        }
                    }
                }
            ]
        }
    }

    response = requests.post(url, headers=HEADERS(), json=filter_params)

    if response.status_code != 200:
        return response.status_code
    else:
        data = []
        for n in response.json()["results"]:
            n_data = {}

            n_data["id"] = n["id"]
            n_data["persona"] = n["properties"]["Persona"]["rich_text"][0]["plain_text"].strip()
            n_data["code"] = n["properties"]["Objeto"]["rollup"]["array"][0]["title"][0]["text"]["content"].strip()
            print(n_data["code"])

            n_data["start_date"] = fromisoformat(n["properties"]["Prestamo"]["date"]["start"])
            if n["properties"]["Devolucion"]["date"] == None:
                n_data["end_date"] = None
            else:
                n_data["end_date"] = fromisoformat(n["properties"]["Devolucion"]["date"]["end"])

            n_data["fee"] = calculate_fee(n_data["start_date"], now)

            data.append(n_data)

        return data

def get_pendient(object, now=now_time()):
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

    filter_params = {
        "filter": {
            "and": [
                {
                "property": "Objeto",
                "rollup": {
                    "any": {
                        "rich_text": {
                            "contains": object
                        }
                    }
                }
                },
                {
                "property": "Estado",
                "formula": {"string": {"contains": "🟠"}}
                }
            ]
        }
    }

    response = requests.post(url, headers=HEADERS(), json=filter_params)

    if response.status_code != 200:
        return response.status_code
    else:
        data = []
        for n in response.json()["results"]:
            n_data = {}

            n_data["id"] = n["id"]
            # n_data["tipo"] = n["properties"]["Tipo"]["formula"]["string"]
            n_data["tipo"] = "nn"
            n_data["persona"] = n["properties"]["Persona"]["rich_text"][0]["plain_text"].strip()
            n_data["code"] = n["properties"]["Codigo"]["title"][0]["text"]["content"].strip()

            n_data["start_date"] = fromisoformat(n["properties"]["Prestamo"]["date"]["start"])
            if n["properties"]["Devolucion"]["date"] == None:
                n_data["end_date"] = None
            else:
                n_data["end_date"] = fromisoformat(n["properties"]["Devolucion"]["date"]["end"])

            n_data["fee"] = calculate_fee(n_data["start_date"], now)

            data.append(n_data)

        return data

def debt_format(data):
    info = f"{data[0]['persona']} TIENE DEUDA: \n"
    for d in data:
        fee = "Sin deuda" if d["fee"] == 0 else f"${d['fee']} 💸"
        info += f' - \t {d["start_date"].day}/{d["start_date"].month}/{d["start_date"].year}\n'
        info += f'\t{d["code"]} : {fee}\n'
    return info

def pay_format(card):
    info = f"""
{card['persona']} tiene una
deuda de ${card['fee']} 💸
por el prestamo de
el dia {card['start_date'].day}/{card['start_date'].month}/{card['start_date'].year}
"""

    return info

def generate_code(PERSON):
    h = datetime.now(timezone.utc)
    return str(PERSON)[4:-1] + h.strftime("%m%d%H%M")

def get_id(code):
    url = f"https://api.notion.com/v1/databases/{INVENTORY_ID}/query"

    filter_params = {
        "filter": {
            "property": "ID",
            "rich_text": {
                "contains": code
            },
        }
    }

    response = requests.post(url, headers=HEADERS(), json=filter_params)
    if response.status_code != 200:
        return response.status_code
    if len(response.json()["results"]) == 0:
        return 0
    return response.json()["results"][0]["id"]