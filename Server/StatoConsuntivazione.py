from sqlalchemy import null
from Stato import Stato
from StatoIniziale import StatoIniziale

class StatoConsuntivazione(Stato):
    """
    ---
    Class Name : StatoConsuntivazione 
    ---
    - Args → Stato (type Stato): rappresenta lo stato
    - Description → Stato che rappresenta un'attività di consuntivazione
    """    
    # costruttore
    def __init__(self):
        self.statoAttuale="consuntivazione"
        self.dati={
          "inizio":"",
          "codice progetto":"",
          "data" :"", 
          "ore fatturabili" :"",
          "ore viaggio":"",
          "ore viaggio fatturabili":"",
          "sede": "",  
          "fatturabile":"",
          "descrizione" : "",
          "conferma" :"",
        }

    def addDati(self, x, y):
        if x in self.dati:
            self.dati[x]=y

    #return: Stato attuale -> str
    def getStatoAttuale(self) -> str:
        """
        ---
        Function Name : getStatoAttuale 
        ---
        - Args → None
        - Description → restituisce lo stato attuale
        - Returns → str value
        """     
        return self.statoAttuale

    #return: i dati delle conversazioni precedenti -> dict
    def getDati(self) -> dict:
        """
        ---
        Function Name : getDati 
        ---
        - Args → None
        - Description → restituisce i dati attualmente inseriti
        - Returns → dictionary values
        """
        return self.dati
