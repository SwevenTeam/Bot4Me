from Stato import Stato


class StatoCancello(Stato):
    """
    ---
    Class Name : StatoCancello 
    ---
    - Args → Stato (type Stato): rappresenta lo stato
    - Description → Stato che rappresenta un'attività di apertura di un cancello
    """   
    def __init__(self):
        super().__init__()
        self.dati = { 'sede': '' }
        self.STATO = 'cancello'

    def getStatoAttuale(self) -> str:
        """
        ---
        Function Name : getStatoAttuale 
        ---
        - Args → None
        - Description → restituisce lo stato attuale
        - Returns → str value
        """ 
        return self.STATO

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

    def addDati(self, key, value):
        if key == 'sede':
            self.dati[key]=value