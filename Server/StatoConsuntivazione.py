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
        self.dati={
          "codice progetto":"",
          "data" :"", 
          "ore fatturabili" :"",
          "ore viaggio":"",
          "ore viaggio fatturabili":"",
          "sede": "",  
          "fatturabile":"",
          "descrizione" : ""
        }
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
            # codice progetto
                self.substate="codice progetto"
            elif(self.substate =="codice progetto") :
                self.dati["codice progetto"]=inputStatement.getText()  
            # data              
                self.substate="data"
            elif(self.substate =="data") :
                self.dati["data"]=inputStatement.getText()
            # ore fatturabili
                self.substate="ore fatturabili"
            elif(self.substate =="ore fatturabili") :
                self.dati["ore fatturabili"]=inputStatement.getText()
            # ore viaggio                
                self.substate="ore viaggio"
            elif(self.substate =="ore viaggio") :
                self.dati["ore viaggio"]=inputStatement.getText()
            # ore viaggio fatturabili
                self.substate="ore viaggio fatturabili"
            elif(self.substate =="ore viaggio fatturabili") :
                self.dati["ore viaggio fatturabili"]=inputStatement.getText() 
            # sede
                self.substate="sede"
            elif(self.substate =="sede") :
                self.dati["sede"]=inputStatement.getText()
            # fatturabile
                self.substate="fatturabile"
            elif(self.substate =="fatturabile") :
                self.dati["fatturabile"]=inputStatement.getText()
            # descrizione
                self.substate="descrizione"
            elif(self.substate =="descrizione") :
                self.dati["descrizione"]=inputStatement.getText()
                self.substate="termina"
               

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
       