import string
from sqlalchemy import Boolean
import requests


def returnAllData(s) -> string:
    sentence = ""
    values = s.getData()
    for x in values:
        sentence += x + " : " + values[x] + "\n"

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
