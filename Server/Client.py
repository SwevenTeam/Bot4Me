from re import S
from sqlalchemy import null
from StatementStato import StatementStato
from StatoPresenzaSede import StatoPresenzaSede
from StatoLogin import StatoLogin

class Client:
    """
    ---
    Class Name : Client
    ---
    - Description → Rappresenta il Client che fa una richiesta al server
    """    
    
    def __init__(self, server):
        self.stato = StatoLogin()
        #self.apiKey = '12345678-1234-1234-1234-123456789012'
        self.apiKey = ''
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
        s = self.server.getResponse(text, self.stato, self.apiKey)
        # nuovo stato
        stato = s.getStato()
        
        if self.stato.getStatoAttuale() and self.stato.getStatoAttuale() != stato.getStatoAttuale()  :
          self.upgradeStato(stato)

        if self.stato.getStatoAttuale() == "Iniziale" and self.apiKey != s.getApiKey():
            self.upgradeApiKey(s.getApiKey())

        return str(s)

    def upgradeStato(self, stato):
        """
        ---
        Function Name : upgradeStato 
        ---
        - Args → stato ( type String) : nuovo stato
        - Description → aggiorna lo stato del Client
        - Returns → None
        """        
        self.stato = stato

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

    def getStato(self) :
        """
        ---
        Function Name : getStato
        ---
        - Args → None
        - Description → restituisce lo stato
        - Returns → Stato value : restituisce lo stato del Client
        """
        return self.stato