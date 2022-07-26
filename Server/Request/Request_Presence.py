from sqlalchemy import false, true
import requests
from requests import Response
from Request.MyRequest import MyRequest


class Request_Presence(MyRequest):
    """
    ---
    Class Name : Request_Presence
    ---
    - Description → Request utilizzata per mandare la richiesta HTTP per effettuare registrazione di presenza
    """

    def __init__(self, s, apiKey):
        self.dati = s.getData()
        self.state = s.getCurrentState()
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
        if self.state == "presenza Sede" and self.Api:
            if self.dati['sede'] != "":
                return True
            else:
                return False
        else:
            return False

    def sendRequest(self, bool=True) -> bool:
        """
        ---
        Function Name : sendRequest
        ---
        - Args → None
        - Description → assembla la richiesta di registrazione presenza e la invia
        - Returns → boolean value : true se ha eseguito, false altrimenti
        """
        url = "https://apibot4me.imolinfo.it/v1/locations/" + \
            self.dati["sede"] + "/presence"
        header = {
            'api_key': self.Api,
            'accept': 'application/json',
            'Content-Type': 'application/json'}
        if bool:
            responseUrl = requests.post(url, headers=header, data={})

            if responseUrl.status_code >= 200 and responseUrl.status_code < 300:
                return True
            else:
                return False
        else:
            responseUrl = requests.delete(url, headers=header, data={})

            if responseUrl.status_code >= 200 and responseUrl.status_code < 300:
                return True
            else:
                return False
