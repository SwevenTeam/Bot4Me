from chatterbot.conversation import Statement
from Stato import Stato

import copy
class StatementStato(Statement):
    """
    ---
    Class Name : StatementStato 
    ---
    - Args → Statement (tipo Statement): statement di Chatbot
    - Description → StatementStato contiene uno Statement di Chatterbot, in aggiunta ad uno stato ed alla API key dell'utente
    """  
    def __init__(self, text, s, apiKey=None, in_response_to=None, **kwargs):
        super().__init__(text, in_response_to, **kwargs)  
        self.stato=s
        self.apiKey = apiKey

    def getApiKey(self):
        """
        ---
        Function Name : getApiKey 
        ---
        - Args → None
        - Description → restituisce la API Key
        - Returns → string value : API key value
        """      
        return self.apiKey

    def getStato(self) -> Stato :
        """
        ---
        Function Name : getStato 
        ---
        - Args → None
        - Description → restituisce lo stato corrente
        - Returns → Stato value
        """     
        return self.stato

    def getText(self) -> str :
        """
        ---
        Function Name : getText 
        ---
        - Args → None
        - Description → restituisce il testo dello statement
        - Returns → string value : testo del messaggio
        """     
        return self.text
