from chatterbot.conversation import Statement
from .State import State

import copy
class Statement_State(Statement):
    """
    ---
    Class Name : Statement_State 
    ---
    - Args → Statement (tipo Statement): statement di Chatbot
    - Description → Statement_State contiene uno Statement di Chatterbot, in aggiunta ad uno stato ed alla API key dell'utente
    """  
    def __init__(self, text, s, apiKey=None, in_response_to=None, **kwargs):
        super().__init__(text, in_response_to, **kwargs)  
        self.currentState=s
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

    def getState(self) -> State :
        """
        ---
        Function Name : getState 
        ---
        - Args → None
        - Description → restituisce lo stato corrente
        - Returns → State value
        """     
        return self.currentState

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
