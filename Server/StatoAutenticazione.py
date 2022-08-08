from sqlalchemy import null
from Stato import Stato
class StatoAutenticazione(Stato):
    
    def __init__(self):
        self.statoAttuale= "Autenticazione"
        self.dati = null

    #return: Stato attuale -> str
    def getStatoAttuale(self):
        return self.statoAttuale

    #return: i dati delle conversazioni precedenti -> dict
    def getDati(self):
        return self.dati