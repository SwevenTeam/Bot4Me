from sqlalchemy import null
from .State import State


class State_Login(State):

    def __init__(self):
        self.currentState = "Login"
        self.data = {"utente": ""}

    # return: Stato attuale -> str
    def getCurrentState(self):
        return self.currentState

    # return: i dati delle conversazioni precedenti -> dict
    def getData(self):
        return self.data

    def addData(self, x, y):
        if x in self.data:
            self.data[x] = y
