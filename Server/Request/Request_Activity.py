from decimal import InvalidOperation
from urllib import response
from xmlrpc.client import Boolean
from chatterbot.logic import LogicAdapter
from State.Statement_State import Statement_State
from State.State_Activity import State_Activity
from chatterbot.conversation import Statement
from sqlalchemy import false, true
import requests
from requests import Response
import json


class Request_Activity():
    """
    ---
    Class Name : Request_Activity
    ---
    - Description → Request utilizzata per mandare la richiesta HTTP per effettuare una consuntivazione
    """

    def __init__(self, s, apiKey):
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
        if self.data["conferma"] == "conferma":
            return True
        else:
            return False

    def sendRequest(self) -> Boolean:
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

        print(responseUrl)

        if responseUrl.status_code >= 200 and responseUrl.status_code < 300:
            return True
        else:
            return False
