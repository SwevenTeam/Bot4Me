from xmlrpc.client import Boolean
from sqlalchemy import false, true
import requests

class Request_Project_Creation():
    """
    ---
    Class Name : Request_Project_Creation
    ---
    - Description → Request utilizzata per mandare la richiesta HTTP per creare un nuovo progetto
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
        - Description → assembla la richiesta di creazione di un nuovo progetto e la invia
        - Returns → boolean value : true se ha eseguito, false altrimenti
        """

        myurl = "https://apibot4me.imolinfo.it/v1/projects/"

        header = {
            'accept': 'application/json',
            'api_key': self.Api,
        }

        informazioni = {
            'code': self.data["codice progetto"],
            'detail': self.data["dettagli"],
            'customer': self.data["cliente"],
            'manager': self.data["manager"],
            'status': self.data["status"],
            'area': self.data["area"],
            'startDate': self.data["data Inizio"],
            'endDate': self.data["data Fine"],
        }

        responseUrl = requests.post(
            url=myurl, headers=header, json=informazioni)

        print(responseUrl)

        if responseUrl.status_code >= 200 and responseUrl.status_code < 300:
            return True
        else:
            return False

    def checkCodeProject(self, code) -> Boolean:
        """
        ---
        Name checkProjectExistance
        ---
        - Args → code (int) : rappresenta il codice del progetto
        - Description → manda una richiesta get e ritorna se il lavoro è presente o meno
        - Returns → boolean value : true se non esite, false altrimenti
        """
        myurl = "https://apibot4me.imolinfo.it/v1/projects/" + code
        header = {'accept': 'application/json', 'api_key': self.Api, }

        response = requests.get(myurl, headers=header, data={})

        if response.status_code >= 200 and response.status_code < 300 and response.headers.get(
                'Content-Length') == "0":
            return True
        else:
            return False
