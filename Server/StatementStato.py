from chatterbot.conversation import Statement
from Stato import Stato
from StatoPresenzaSede import StatoPresenzaSede
import copy
class StatementStato(Statement):
    def __init__(self, text, s, apiKey=None, in_response_to=None, **kwargs):
        super().__init__(text, in_response_to, **kwargs)
        self.stato=s
        self.apiKey = apiKey

    def getApiKey(self):
        return self.apiKey

    def getStato(self):
        return self.stato
