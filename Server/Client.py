from re import S
from sqlalchemy import null
from State.State_Null import State_Null

class Client:
    """
    ---
    Class Name : Client
    ---
    - Description → Rappresenta il Client che fa una richiesta al server
    """

    def __init__(self, server):
        self.state = State_Null()
        self.apiKey = null
        self.server = server

    def getResponse(self, text):
        """
        ---
        Function Name :  getResponse
        ---
        - Args → text ( type String) : frase in input inviata dall'utente
        - Description → invia il messaggio al server e restituisce la risposta
        - Returns → string value : restituisce la risposta del server
        """
        server_response = self.server.getResponse(text, self.state, self.apiKey)
        # nuovo stato
        updated_state = server_response.getState()
        if self.state != updated_state:
          self.upgradeState(updated_state)

        if self.state.getCurrentState() == "Iniziale" and self.apiKey != server_response.getApiKey():
            self.upgradeApiKey(server_response.getApiKey())

        return str(server_response)

    def upgradeState(self, state):
        """
        ---
        Function Name : upgradeState 
        ---
        - Args → stato ( type String) : nuovo stato
        - Description → aggiorna lo stato del Client
        - Returns → None
        """        
        self.state = state

    def upgradeApiKey(self, apiKey):
        """
        ---
        Function Name : upgradeApiKey 
        ---
        - Args → apiKey ( type String) : nuova API Key
        - Description → aggiorna la ApiKey
        - Returns → None
        """  
        self.apiKey=apiKey
