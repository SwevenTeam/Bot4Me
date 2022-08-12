from decimal import InvalidOperation
from chatterbot.logic import LogicAdapter
from StatementStato import StatementStato
from StatoConsuntivazione import StatoConsuntivazione
from chatterbot.conversation import Statement
from sqlalchemy import false, true
import requests
from requests import Response

class RequestPresenza():
    """
    ---
    Class Name : RequestPresenza 
    ---
    - Description → Request utilizzata per mandare la richiesta HTTP per effettuare registrazione di presenza
    """
    def __init__(self, s, apiKey):
        self.dati = s.getDati()
        self.ready = s.getStatoAttuale()
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
        if self.ready=="presenza Sede":
            if self.dati :
                return True
            else : 
                return False
        else:
            return False

    def sendRequest(self) :
        """
        ---
        Function Name : sendRequest
        ---
        - Args → None
        - Description → assembla la richiesta di registrazione presenza e la invia
        - Returns → boolean value : true se ha eseguito, false altrimenti
        """     
        # L'url credo sia giusto così
        url = "https://apibot4me.imolinfo.it/v1/locations/" + self.dati["sede"] + "/presence"
        header={'api_key': self.Api, 'accept': 'application/json', 'Content-Type': 'application/json'}

        responseUrl = requests.post(url, headers=header, data={})

        if responseUrl.status_code >= 200 and responseUrl.status_code <300:
          return True
        else:
          return False