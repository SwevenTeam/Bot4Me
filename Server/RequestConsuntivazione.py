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

        myurl = "https://apibot4me.imolinfo.it/v1/projects/"+ self.dati["codice progetto"]+"/activities/me"

        header={ 'accept': 'application/json','api_key': self.Api, 'Content-Type': 'application/json'}
        
        informazioni=[
            {
              'date': self.dati["data"],
              'billableHours': self.dati["ore fatturabili"],
              'travelHours': self.dati["ore viaggio"],
              'billableTravelHours': self.dati["ore viaggio fatturabili"],
              'location': self.dati["sede"],
              'billable': self.dati["fatturabile"],
              'note': self.dati["descrizione"]
            },
          ]


        responseUrl = requests.post(
          url = myurl, 
          headers = header, 
          json = informazioni          
        )

        print(responseUrl)
        
        if responseUrl.status_code >=200 and responseUrl.status_code <300 :
            return True
        else :
            return False

    def checkProjectExistance(self, code) -> Boolean :
        """
        ---
        Name checkProjectExistance 
        ---
        - Args → code (int) : rappresenta il codice del progetto
        - Description → manda una richiesta get e ritorna se il lavoro è presente o meno
        - Returns → boolean value : true se esite, false altrimenti
        """        
        myurl = "https://apibot4me.imolinfo.it/v1/projects/" + code
        header = { 'accept': 'application/json','api_key': self.Api,}

        response = requests.get(myurl,headers=header,data={})
        
        if response.status_code >=200 and response.status_code < 300 :
          return True
        else :
          return False