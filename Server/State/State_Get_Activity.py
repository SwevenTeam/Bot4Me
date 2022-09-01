from sqlalchemy import null
from .State import State


class State_Get_Activity(State):
    """
    ---
    Class Name : State_Get_Activity
    ---
    - Args → Stato (type Stato): rappresenta lo stato
    - Description → Stato che rappresenta la restituzione di una consuntivazione
    """
    # costruttore

    def __init__(self):
        self.currentState = "restituzione consuntivazione"
        self.data = {
            "codice progetto": ""
        }

    def addData(self, x, y):
        if x in self.data:
            self.data[x] = y

    # return: Stato attuale -> str
    def getCurrentState(self) -> str:
        """
        ---
        Function Name : getCurrentState
        ---
        - Args → None
        - Description → restituisce lo stato attuale
        - Returns → str value
        """
        return self.currentState

    # return: i dati delle conversazioni precedenti -> dict
    def getData(self) -> dict:
        """
        ---
        Function Name : getData
        ---
        - Args → None
        - Description → restituisce i dati attualmente inseriti
        - Returns → dictionary values
        """
        return self.data
