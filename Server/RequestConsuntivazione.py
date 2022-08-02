from decimal import InvalidOperation
from urllib import response
from xmlrpc.client import Boolean
from chatterbot.logic import LogicAdapter
from StatementStato import StatementStato
from StatoConsuntivazione import StatoConsuntivazione
from chatterbot.conversation import Statement
from sqlalchemy import false, true
import requests
from requests import Response
import json

class RequestConsuntivazione():
    """
    ---
    Class Name : RequestConsuntivazione 
    ---
    - Description → Request utilizzata per mandare la richiesta HTTP per effettuare una consuntivazione
    """
    def __init__(self, s, apiKey):
        self.dati = s.getDati()
        self.ready = s.getSubstate()
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
        if(self.ready=="termina"):
          return True
        else:
          return False

    def sendRequest(self) -> Boolean :
        """
        ---
        Function Name : sendRequest
        ---
        - Args → None
        - Description → assembla la richiesta di consuntivazione e la invia
        - Returns → boolean value : true se ha eseguito, false altrimenti
        """      
        # il code da dove cazzo lo tiro fuori?
        url = "https://apibot4me.imolinfo.it/v1/projects/1/activities/me"
        headers={"api_key": self.Api, 'accept': 'application/json', 'Content-Type': 'application/json'}
        data={'date': self.dati["data"],
            'billableHours': self.dati["durata"],
            'travelHours': 0,
            'billableTravelHours': 0,
            'location': self.dati["Sede"],
            'billable': true,
            'note': self.dati["descrizione"]}
        responseUrl = requests.post(
          url, 
          headers, 
          data
          )
        if responseUrl : 
          #responseUrl == 200:
          return True
        else:
          return False
