from params import DAY_PRICE, MAX_PRICE
from env import DATABASE_ID, HEADERS
import requests
from datetime import datetime, timedelta, datetime, timezone
fromisoformat = datetime.fromisoformat
now_time = lambda : datetime.now(timezone.utc)



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
                "rich_text": {"contains": person[:-2]},
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
            n_data["tipo"] = n["properties"]["Tipo"]["formula"]["string"]
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

def get_pendient(object, now=now_time()):
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

    filter_params = {
        "filter": {
            "and": [
                {
                "property": "Codigo",
                "rich_text": {"contains": object},
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
        info += f' - {d["tipo"]} \t {d["start_date"].day}/{d["start_date"].month}/{d["start_date"].year}\n'
        info += f'\t{d["code"]} : {fee}\n'
    return info

def pay_format(card):
    info = f"""
{card['persona']} tiene una
deuda de ${card['fee']} 💸
por el prestamo de
un(a) {card['tipo']}
el dia {card['start_date'].day}/{card['start_date'].month}/{card['start_date'].year}
"""

    return info