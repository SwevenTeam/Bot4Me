from sqlalchemy import null
from Stato import Stato
from StatoIniziale import StatoIniziale
class StatoConsuntivazione(Stato):
    
    # costruttore
    def __init__(self):
        self.statoAttuale="consuntivazione"
        self.dati={"Sede": "", "descrizione" : "", "data" :"", "durata" :""}
        self.substate="inizio"

    # cambiare valori di d con dati della consuntivazione
    def aggiornamento(self,inputStatement):
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
    def getStatoAttuale(self):
        return self.statoAttuale

    #return: i dati delle conversazioni precedenti -> dict
    def getDati(self):
        return self.dati

    def getSubstate(self):
        return self.substate
       