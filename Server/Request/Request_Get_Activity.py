from xmlrpc.client import Boolean
from sqlalchemy import false, true
import requests
from requests import Response
import json
from datetime import date
from .Util_Request import IsDictionaryFilled, parseResponseGetActivity
from Request.MyRequest import MyRequest


class Request_Get_Activity(MyRequest):
    """
    ---
    Class Name : Request_Activity
    ---
    - Description → Request utilizzata per mandare la richiesta HTTP per effettuare una consuntivazione
    """

    def __init__(self, s, apiKey):
        self.state = s.getCurrentState()
        self.data = s.getData()
        self.Api = apiKey

    def isReady(self) -> bool:
        """
        ---
        Function Name : isReady
        ---
        - Args → None
        - Description → identifica se questa Request può essere utilizzata
        - Returns → boolean value : true se può eseguire, false se non può eseguire
        """
        if self.state == "restituzione consuntivazione":
            if IsDictionaryFilled(self.data):
                return True
            else:
                return False
        else:
            return False

    def sendRequest(self) -> bool:
        """
        ---
        Function Name : sendRequest
        ---
        - Args → None
        - Description → assembla la richiesta di consuntivazione e la invia
        - Returns → boolean value : true se ha eseguito, false altrimenti
        """

        myurl = "https://apibot4me.imolinfo.it/v1/projects/" + \
            self.data["codice progetto"] + "/activities/me"

        header = {
            'accept': 'application/json',
            'api_key': self.Api,
            'Content-Type': 'application/json'}

        today = date.today().strftime('%Y-%m-%d')

        informazioni = {
            'from': self.data["data"],
            'to': today
        }

        print(today)

        responseUrl = requests.get(
            url=myurl,
            headers=header,
            params=informazioni
        )

        if responseUrl.status_code >= 200 and responseUrl.status_code < 300:
            return parseResponseGetActivity(responseUrl.json())
        else:
            return []
