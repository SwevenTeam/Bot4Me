from sqlalchemy import null
from .State import State


class State_Project_Creation(State):
    """
    ---
    Class Name : State_Project_Creation
    ---
    - Args → Stato (type Stato): rappresenta lo stato
    - Description → Stato che rappresenta un'attività di creazione di un Nuovo Progetto
    """

    def __init__(self):
        self.currentState = "creazione progetto"
        self.data = {
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

    # return: Stato attuale -> str
    def getCurrentState(self):
        """
        ---
        Function Name : getCurrentState
        ---
        - Args → None
        - Description → restituisce lo stato attuale
        - Returns → str value : rappresenta lo stato attuale della Presenza
        """
        return self.currentState

    # return: i dati delle conversazioni precedenti -> dict
    def getData(self):
        """
        ---
        Function Name : getData
        ---
        - Args → None
        - Description → restituisce i dati attualmente inseriti
        - Returns → dictionary values : rappresentano i dati salvati all'interno dello stato
        """
        return self.data

    def addData(self, x, y):
        if x in self.data:
            self.data[x] = y
