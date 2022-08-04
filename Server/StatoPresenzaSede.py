from sqlalchemy import null
from Stato import Stato

class StatoPresenzaSede(Stato):
    """
    ---
    Class Name : StatoConsuntivazione 
    ---
    - Args → Stato (type Stato): rappresenta lo stato
    - Description → Stato che rappresenta un'attività di consuntivazione
    """   
    def __init__(self):
        self.statoAttuale="presenza Sede"
        self.dati={"sede": ""}

    #return: Stato attuale -> str
    def getStatoAttuale(self):
        """
        ---
        Function Name : getStatoAttuale 
        ---
        - Args → None
        - Description → restituisce lo stato attuale
        - Returns → str value : rappresenta lo stato attuale della Presenza
        """     
        return self.statoAttuale

    #return: i dati delle conversazioni precedenti -> dict
    def getDati(self):
        """
        ---
        Function Name : getDati 
        ---
        - Args → None
        - Description → restituisce i dati attualmente inseriti
        - Returns → dictionary values : rappresentano i dati salvati all'interno dello stato
        """
        return self.dati

    def addNomeSede(self, x):
        self.dati["sede"] = x

    def addDati(self, x, y):
        if x in self.dati:
            self.dati[x]=y
