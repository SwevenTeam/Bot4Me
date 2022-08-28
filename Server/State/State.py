class State:
    def __init__(self):
        pass

    # return: Stato attuale -> str
    def getCurrentState(self) -> str:
        pass

    # return: i dati delle conversazioni precedenti -> dict
    def getData(self):
        pass

    #param x: nome del dato da inserire
    #param y: valore del dato da inserire
    def addData(self, x, y):
        pass
