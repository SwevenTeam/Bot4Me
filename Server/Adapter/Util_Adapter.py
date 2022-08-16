import string
from tokenize import String
from sqlalchemy import Boolean
import requests
from difflib import SequenceMatcher


def returnAllData(s) -> string:
    sentence = ""
    values = s.getData()
    for x in values:
        sentence += x + " : " + values[x] + "<br>"

    return sentence


def checkCodeProject(code, Api) -> Boolean:
    """
    ---
    Name checkProjectExistance
    ---
      - Args → code (int) : rappresenta il codice del progetto
      - Description → manda una richiesta get e ritorna se il lavoro è presente o meno
      - Returns → boolean value : true se non esite, false altrimenti
    """
    myurl = "https://apibot4me.imolinfo.it/v1/projects/" + code
    header = {'accept': 'application/json', 'api_key': Api, }

    response = requests.get(myurl, headers=header, data={})

    if response.status_code >= 200 and response.status_code < 300 and response.headers.get(
            'Content-Length') == "0":
        return True
    else:
        return False


def checkProjectExistance(code, Api) -> Boolean:
    """
    ---
    Name checkProjectExistance
    ---
    - Args → code (int) : rappresenta il codice del progetto
    - Description → manda una richiesta get e ritorna se il lavoro è presente o meno
    - Returns → boolean value : true se esite, false altrimenti
    """
    myurl = "https://apibot4me.imolinfo.it/v1/projects/" + code
    header = {'accept': 'application/json', 'api_key': Api, }

    response = requests.get(myurl, headers=header, data={})

    if response.status_code >= 200 and response.status_code < 300 and response.headers.get(
            'Content-Length') != "0":
        return True
    else:
        return False


def similarStringMatch(Statement, Dict) -> Boolean:

    for y in Dict:
        y_lower = y.lower()
        for x in Statement:
            x_lower = x.lower()
            if SequenceMatcher(None, x_lower, y_lower).ratio() >= 0.80:
                return True
    return False


def similarStringMatch_Location(Statement, Api) -> String:

    for y in getLocationList(Api):
        y_lower = y.lower()
        for x in Statement:
            x_lower = x.lower()
            if SequenceMatcher(None, x_lower, y_lower).ratio() >= 0.80:
                return y_lower
    return ''


def getLocationList(Api):
    url = 'https://apibot4me.imolinfo.it/v1/locations'
    header = {'accept': 'application/json', 'api_key': Api}

    responseUrl = requests.get(url, headers=header)

    if responseUrl.status_code >= 200 and responseUrl.status_code < 300:
        return [data["name"] for data in responseUrl.json()]
    return []
