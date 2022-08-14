from sqlalchemy import null
from .State import State

class State_Presence(State):
    """
    ---
    Class Name : State_Presence 
    ---
    - Args → Stato (type Stato): rappresenta lo stato
    - Description → Stato che rappresenta un'attività di consuntivazione
    """   
    def __init__(self):
        self.currentState="presenza Sede"
        self.data={"sede": ""}

    #return: Stato attuale -> str
    def getCurrentState(self) -> str:
        """
        ---
        Function Name : getCurrentState 
        ---
        - Args → None
        - Description → restituisce lo stato attuale
        - Returns → str value : rappresenta lo stato attuale della Presenza
        """     
        return self.currentState

    #return: i dati delle conversazioni precedenti -> dict
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
            self.data[x]=y

