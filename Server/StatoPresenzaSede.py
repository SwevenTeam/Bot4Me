from sqlalchemy import null
from Stato import Stato
class StatoPresenzaSede(Stato):
    
    def __init__(self, s="presenzaSede",d={"nomeSede": ""}):
            self.statoAttuale=s
            self.dati=d

    #return: Stato attuale -> str
    def getStatoAttuale(self):
        return self.statoAttuale

    #return: i dati delle conversazioni precedenti -> dict
    def getDati(self):
        return self.dati