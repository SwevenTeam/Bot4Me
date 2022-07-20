from sqlalchemy import null
from Stato import Stato
class StatoPresenzaSede(Stato):
    
    def __init__(self):
        self.statoAttuale = "presenzaSede"
        self.apiKey = null
        self.dati = {
            "nomeSede": "",
        }

    def __init__(self, s: Stato):
        self.attualeStato = s.getStatoAttuale()
        self.apiKey = s.getApiKey()
        self.dati = s.getDati()

    #return: Stato attuale -> str
    def getStatoAttuale(self):
        return self.statoAttuale
    
    #return: null se untente non logato, atrimenti il suo apikey -> str
    def getApiKey(self): 
        return self.apiKey

    #return: i dati delle conversazioni precedenti -> dict
    def getDati(self): 
        return self.dati