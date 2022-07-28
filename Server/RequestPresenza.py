from decimal import InvalidOperation
from chatterbot.logic import LogicAdapter
from StatementStato import StatementStato
from StatoConsuntivazione import StatoConsuntivazione
from chatterbot.conversation import Statement
from sqlalchemy import false, true
import requests
from requests import Response

class RequestPresenza():
    def __init__(self, s, apiKey):
        self.dati = s.getDati()
        self.ready = s.getStato()
        self.Api = apiKey

    def isReady(self) -> bool:
        if self.ready=="presenza Sede":
          if self.dati :
            return True
          else : 
            return False
        else:
          return False

    def sendRequest(self) :
        # url = "https://apibot4me.imolinfo.it/v1/projects/"+  +"/activities/me"
        return "cazzo"
        #return response_statement
