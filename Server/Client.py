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
        self.upgradeStato(s.getStato())
        self.upgradeApiKey(s.getApiKey())
        return str(s)

    def upgradeStato(self, stato):
        self.stato = stato

    def upgradeApiKey(self, apiKey):
        self.apiKey=apiKey