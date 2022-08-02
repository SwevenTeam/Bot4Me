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
        self.dati={"Sede": "", "descrizione" : "", "data" :"", "durata" :""}
        self.substate="inizio"

    # cambiare valori di d con dati della consuntivazione
    def aggiornamento(self,inputStatement):
        """
        ---
        Function Name : aggiornamento 
        ---
        - Args → inputStatement (type StatementStato): input dell'utente con stato attuale del Client
        - Description → aggiorna il sottostato di StatoConsuntivazione
        - Returns → None
        """    
        if(self.substate):
            if(self.substate =="inizio") :
                self.substate="Sede"
            elif(self.substate =="Sede") :
                self.dati["Sede"]=inputStatement.getText()                
                self.substate="descrizione"
            elif(self.substate =="descrizione") :
                self.dati["descrizione"]=inputStatement.getText()
                self.substate="data"
            elif(self.substate =="data") :
                self.dati["data"]=inputStatement.getText()                
                self.substate="durata"
            elif(self.substate =="durata") :
                self.dati["durata"]=inputStatement.getText()
                self.substate = "termina"
            elif(self.substate =="termina"):
                print("bro")
            else:
                self.substate= "errore"

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

    def getSubstate(self) -> str:
        """
        ---
        Function Name : getSubstate 
        ---
        - Args → None
        - Description → restituisce il sottostato attuale
        - Returns → str value
        """     
        return self.substate
       