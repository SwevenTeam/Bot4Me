from sqlalchemy import null
from Stato import Stato
class StatoPresenzaSede(Stato):
    
    def __init__(self):
            self.statoAttuale="presenza Sede"
            self.dati={"sede": ""}

    #return: Stato attuale -> str
    def getStatoAttuale(self):
        return self.statoAttuale

    #return: i dati delle conversazioni precedenti -> dict
    def getDati(self):
        return self.dati

    def addNomeSede(self, x):
        self.dati["sede"] = x

    def addDati(self, x, y):
        if x in self.dati:
            self.dati[x]=y
