from sqlalchemy import null
from .State import State

class State_Null(State):
    
    def __init__(self):
        self.currentState= "Iniziale"
        self.data = null

    #return: Stato attuale -> str
    def getCurrentState(self):
        return self.currentState

    #return: i dati delle conversazioni precedenti -> dict
    def getData(self):
        return self.data