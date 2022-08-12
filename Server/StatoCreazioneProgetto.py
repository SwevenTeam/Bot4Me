from sqlalchemy import null
from Stato import Stato

class StatoCreazioneProgetto(Stato):
    """
    ---
    Class Name : StatoCreazioneProgetto 
    ---
    - Args → Stato (type Stato): rappresenta lo stato
    - Description → Stato che rappresenta un'attività di creazione di un Nuovo Progetto
    """   
    def __init__(self):
        self.statoAttuale="creazione progetto"
        self.dati={  
          "inizio":"",
          "codice progetto": "",
          "dettagli": "",
          "cliente": "",
          "manager": "",
          "status": "iniziale",
          "area": "",
          "data Inizio": "",
          "data Fine": "",
          "conferma": "non confermato"
          }
    
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

    def addDati(self, x, y):
        if x in self.dati:
            self.dati[x]=y
