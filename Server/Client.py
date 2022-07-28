from re import S
from sqlalchemy import null
from StatementStato import StatementStato
from StatoPresenzaSede import StatoPresenzaSede
from StatoIniziale import StatoIniziale

class Client:
    def __init__(self, server):
        self.stato = StatoIniziale()
        self.apiKey = null
        self.server = server

    def getResponse(self, text):

        s = self.server.getResponse(text, self.stato, self.apiKey)

        nuovoStato = s.getStato()
        
        if self.stato.getStatoAttuale() and self.stato.getStatoAttuale() != nuovoStato.getStatoAttuale()  :
          self.upgradeStato(nuovoStato)
          self.upgradeApiKey( s.apiKey)

        return str(s)

    def upgradeStato(self, newstato):
        #print(self.stato)
        self.stato = newstato

    def upgradeApiKey(self, apiKey):
        self.apiKey=apiKey

    def getStato(self) :
        return self.stato