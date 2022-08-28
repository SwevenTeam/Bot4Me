import json
import requests
from Request import Request

class RequestCancello(Request):

    def __init__(self, api_key) -> None:
        self.sede = ''
        self.APIKEY = api_key

    def isReady(self) -> bool:
        """
        ---
        Function Name : isReady 
        ---
        - Args → None
        - Description → identifica se questa Request può essere utilizzata
        - Returns → boolean value : true se può eseguire, false se non può eseguire
        """
        return self.sede != ''

    def sendRequest(self) -> bool:
        """
        ---
        Function Name : sendRequest
        ---
        - Args → None
        - Description → assembla la richiesta di apertura del cancello e la invia
        - Returns → boolean value : true se ha eseguito, false altrimenti
        """
        # da cambiare URL con quello reale
        URL = 'https://apibot4me.imolinfo.it/v1/locations/' + self.sede + '/devices/cancello/status'
        HEADERS={'accept': 'application/json','api_key': self.APIKEY, 'Content-Type': 'application/json'}
        DATA = {'open': 'string'}

        responseUrl = requests.put(URL, headers=HEADERS, data=DATA)

        if responseUrl.status_code >= 200 and responseUrl.status_code < 300:
            return True
        
        return False

    def setSede(self, stato):
        """
        ---
        Function Name : setSede
        ---
        - Args → 
          - stato ( type Stato): stato dell'operazione in corso
        - Description → imposta la sede per l'apertura del cancello
        - Returns → None
        """
        self.sede = stato.getDati()["sede"]

    def getLocations(self):
        """
        ---
        Function Name : getLocations
        ---
        - Args → None
        - Description → richiede le possibili sedi in cui aprire un cancello
        - Returns → list value : ritorna una lista di tutte le sedi, oppure None in caso di errore
        """

        URL = 'https://apibot4me.imolinfo.it/v1/locations'
        HEADERS = {'accept': 'application/json', 'api_key': self.APIKEY}

        responseUrl = requests.get(URL, headers=HEADERS)

        if responseUrl.status_code >= 200 and responseUrl.status_code < 300:
            return [data["name"] for data in responseUrl.json()]
            
        return []
