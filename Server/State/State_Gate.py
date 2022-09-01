from .State import State


class State_Gate(State):
    """
    ---
    Class Name : StateGate
    ---
    - Args → Stato (type State): rappresenta lo stato
    - Description → Stato che rappresenta un'attività di apertura di un cancello
    """

    def __init__(self):
        super().__init__()
        self.currentState = "cancello"
        self.data = {"sede": ''}

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

    def addData(self, x, y):
        if x in self.data:
            self.data[x] = y
