from decimal import InvalidOperation
from chatterbot.logic import LogicAdapter
from StatementStato import StatementStato
from StatoConsuntivazione import StatoConsuntivazione
from chatterbot.conversation import Statement
from sqlalchemy import false, true
import requests
from requests import Response

class RequestLogin():
    def __init__(self, s, apiKey):
        self.dati = s.getDati()
        self.ready = s.getStatoAttuale()
        self.Api = apiKey

    def isReady(self) -> bool:
        if self.ready=="login":
          if self.dati :
            return True
          else : 
            return False
        else:
          return False

    def sendRequest(self) :
        
        # L'url credo sia giusto così
        url = "https://apibot4me.imolinfo.it/v1/locations/" + \
                self.dati["sede"] + "/presence"

        responseUrl = requests.post(url, headers={"api_key": self.api_key})
            
        if responseUrl == 200:
          return True
        else:
          return False
