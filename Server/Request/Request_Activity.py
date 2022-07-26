from xmlrpc.client import Boolean
from sqlalchemy import false, true
import requests
from requests import Response
import json
from .Util_Request import IsDictionaryFilled
from Request.MyRequest import MyRequest


class Request_Activity(MyRequest):
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
        if self.state == "consuntivazione" and self.Api:
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

        informazioni = [
            {
                'date': self.data["data"],
                'billableHours': self.data["ore fatturabili"],
                'travelHours': self.data["ore viaggio"],
                'billableTravelHours': self.data["ore viaggio fatturabili"],
                'location': self.data["sede"],
                'billable':('True') if self.data["fatturabile"] else ('False'),
                'note': self.data["descrizione"]
            },
        ]

        responseUrl = requests.post(
            url=myurl,
            headers=header,
            json=informazioni
        )

        if responseUrl.status_code >= 200 and responseUrl.status_code < 300:
            return True
        else:
            return False
