from chatterbot.conversation import Statement
from Stato import Stato
class StatementStato(Statement):
    def __init__(self, text, s: Stato, in_response_to=None, **kwargs):
        super.__init__(self, text, in_response_to=None, **kwargs)
        self.stato = s

    def getStato(self):
        return self.stato
    
    def prova(self):
        print(self.stato.getStatoAttuale() + self.stato.getApiKey() + "ciao")