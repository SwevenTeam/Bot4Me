from ast import And
from decimal import InvalidOperation
import string
from chatterbot.logic import LogicAdapter
from RequestConsuntivazione import RequestConsuntivazione
from StatementStato import StatementStato
from StatoConsuntivazione import StatoConsuntivazione
from sqlalchemy import false, null, true
from StatoIniziale import StatoIniziale
import datetime

class AdapterConsuntivazione(LogicAdapter):
    """
    ---
    Class Name : AdapterConsuntivazione
    ---
    - Args → LogicAdapter ( type LogicAdapter) : implementata da tutti gli adapter di Chatbot
    - Description → Adapter utilizzato per effettuare una consuntivazione
    """
    ### Costruttore 
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    
    ### can_process
    ### input : self, frase input presa dal client
    ### output : boolean, true se può eseguire, false se non può eseguire
    def can_process(self, statement):
        """
        ---
        Function Name :  can_process
        ---
        - Args → statement ( type StatementStato) : frase input presa dal client
        - Description → restituisce True se l'elemento in Input contiene keyword corretta o stato uguale a Consuntivazione
        - Returns → boolean value : true se può eseguire, false se non può eseguire
        """
        # Stato per fare i controlli
        stato=statement.getStato()

        if statement.getApiKey() == null :
            return False

        # Se lo Stato è settato a "Iniziale", controllo se l'utente ha inserito consuntivo
        if stato.getStatoAttuale() == "Iniziale":

            # Controllo su presenza stringhe che identificano la richiesta di consuntivazione
            words = ['consuntivazione', 'consuntivare','con', 'consuntiva', 'consuntivo']
            if any(x in statement.text.split() for x in words):
              return True
            else:
              return False

        # Altrimenti, controllo se lo stato è consuntivazione
        elif stato.getStatoAttuale() == "consuntivazione":
            return True

        # Infine, se nessuno dei due if restituiscono vero, questo adapter non potrà effettuare il process
        else:
            return False


    ### process
    ### input : self, frase input presa dal client, ( eventuali info extra )
    ### output : StatementStato, varia in base a quale operazione si sta eseguendo
    def process(self, input_statement, additional_response_selection_parameters) -> StatementStato:
        """
        ---
        Function Name :  process
        ---
        - Args → 
          - input_statement ( type StatementStato): frase inserita dall'utente
          - additional_response_selection_parameters ( type any): elementi extra necessari alla funzione del metodo
        - Description → 
        crea un outputStatement (StatementStato) in base all'input inserito dall'utente 
        - Returns → StatementStato value : risposta del chatbot con eventuale cambio di stato
        """                            
        # s rappresenta lo StatementStato

        s = input_statement.getStato()
        Api = input_statement.getApiKey()
        testo = input_statement.getText()
      
        # Nel caso in cui sia settato ad "Iniziale", 
        # riassegno il valore come una nuova inizializzazione di  StatoConsuntivazione
        if s.getStatoAttuale() and s.getStatoAttuale() == "Iniziale":
            s = StatoConsuntivazione()

        dati = s.getDati()
                    
        # Effettuo dei controlli sul Substate, per sapere cosa dover richiedere all'utente     
        if not dati["inizio"] :
        # if(s.substate =="inizio"):
            s.addDati("inizio",testo)
            output_statement=StatementStato("Consuntivazione Avviata : Inserire il codice del Progetto",s)

        # Utente ha iniziato il processo, Adapter richiede di Inserire il codice del Progetto
        # o Utente vuole modificare il codice del progetto
        elif ( not dati["codice progetto"] and dati["inizio"] ) or dati["conferma"]=="codice progetto":
            # Controllo se il progetto esiste
            Req = RequestConsuntivazione(s,Api)
            if Req.checkProjectExistance( testo) :
                s.addDati("codice progetto",testo)
                # Se è un'operazione di modifica
                if dati["conferma"]=="codice progetto":
                    s.addDati("conferma","non confermato")
                    output_statement=StatementStato("Progetto esistente e dato aggiornato. Visualizzazione Dati Aggiornati \n " + self.returnAllData(s) +"Confermare operazione di consuntivazione?",s)
                # Se è un'operazione di primo inserimento
                else:
                    output_statement=StatementStato("Progetto esistente \n Inserire la data di consuntivazione ( formato aaaa-mm-gg )",s)
            else :
                output_statement=StatementStato("Progetto non esistente \n Reinserire un codice diverso o creare un nuovo progetto",s)
        
        # Utente ha inserito il codice e questo esiste, ora dovrà inserire la data
        elif (not dati["data"] and dati["codice progetto"] ) or dati["conferma"]=="data":
            ### Formato aaaa-mm-gg
            try:
                datetime.datetime.strptime(testo, '%Y-%m-%d')
                s.addDati("data",testo)
                # Se è un'operazione di modifica
                if dati["conferma"]=="data":
                    s.addDati("conferma","non confermato")
                    output_statement=StatementStato("Data accettata e aggiornata. Visualizzazione Dati Aggiornati \n" + self.returnAllData(s) +"Confermare operazione di consuntivazione?",s)
                # Se è un'operazione di primo inserimento
                else:
                    output_statement=StatementStato("Data accettata : Inserire le ore fatturabili",s)
            except ValueError:
                output_statement=StatementStato("Data non accettata : Reinserire la data del progetto",s)
             
        # Utente ha inserito la data nel formato corretto, ora dovrà inserire le ore fatturabili
        elif (not dati["ore fatturabili"] and dati["data"] ) or dati["conferma"]=="ore fatturabili":
            if testo.isnumeric() :
                s.addDati("ore fatturabili",testo)
                # Se è un'operazione di modifica
                if dati["conferma"]=="ore fatturabili":
                    s.addDati("conferma","non confermato")
                    output_statement=StatementStato("Ore Fatturabili accettate e aggiornate. Visualizzazione Dati Aggiornati \n" + self.returnAllData(s) +"Confermare operazione di consuntivazione?",s)
                # Se è un'operazione di primo inserimento
                else:
                    output_statement=StatementStato("Ore fatturabili accettate : Inserire le ore di viaggio",s)
            else:
                output_statement=StatementStato("Ore fatturabili non accettate : Reinserire le ore fatturabili come numero",s)

        # Utente ha inserito il codice e questo esiste, ora dovrà inserire la data
        elif (not dati["ore viaggio"] and dati["ore fatturabili"]) or dati["conferma"]=="ore viaggio":
            if testo.isnumeric() :
                s.addDati("ore viaggio",testo)
                # Se è un'operazione di modifica
                if dati["conferma"]=="ore viaggio":
                    s.addDati("conferma","non confermato")
                    output_statement=StatementStato("Ore di viaggio accettate e aggiornate. Visualizzazione Dati Aggiornati " + self.returnAllData(s) +"Confermare operazione di consuntivazione?",s)
                # Se è un'operazione di primo inserimento
                else :
                    output_statement=StatementStato("Ore viaggio accettate : Inserire le ore di viaggio fatturabili",s)
            else:
                output_statement=StatementStato("Ore viaggio non accettate : Reinserire le ore di viaggio come numero",s)


        # Utente ha inserito il codice e questo esiste, ora dovrà inserire la data
        elif ( not dati["ore viaggio fatturabili"] and dati["ore viaggio"]) or dati["conferma"]=="ore viaggio fatturabili":
            if testo.isnumeric() :
              s.addDati("ore viaggio fatturabili",testo)
              # Se è un'operazione di modifica
              if dati["conferma"]=="ore viaggio":
                  s.addDati("conferma","non confermato")
                  output_statement=StatementStato("Ore di viaggio fatturabili accettate e aggiornate. Visualizzazione Dati Aggiornati " + self.returnAllData(s) +" Confermare operazione di consuntivazione?",s)
              # Se è un'operazione di primo inserimento
              else :
                output_statement=StatementStato("ore viaggio fatturabili Accettate : Inserire la sede",s)
            else:
              output_statement=StatementStato("Ore viaggio fatturabili non accettate : Reinserire le ore di viaggio fatturabili come numero",s)


        # Controllo quindi se nel messaggio inviato dall'utente sia presente una delle due Sedi
        elif ( not dati["sede"] and dati["ore viaggio fatturabili"]) or dati["conferma"]=="sede":
            sedeP = ['Bologna', 'bologna','bl']
            sedeI = ['Imola', 'imola', 'im']
            if any(x in testo.split() for x in sedeP):
                s.addDati("sede","Bologna")
                # Se è un'operazione di modifica
                if dati["conferma"]=="sede" :
                    s.addDati("conferma","non confermato")
                    output_statement=StatementStato("Sede Accettata e aggiornata. Visualizzazione Dati Aggiornati \n " + self.returnAllData(s) +" Confermare operazione di consuntivazione?",s)
                # Se è un'operazione di primo inserimento
                else:
                    output_statement=StatementStato("Sede Accettata : È fatturabile?",s)
            elif any(x in testo.split() for x in sedeI):
                s.addDati("sede","Imola")
                # Se è un'operazione di modifica
                if dati["conferma"]=="sede" :
                    s.addDati("conferma","non confermato")
                    output_statement=StatementStato("Sede Accettata e aggiornata. Visualizzazione Dati Aggiornati \n " + self.returnAllData(s) +" Confermare operazione di consuntivazione?",s)
                # Se è un'operazione di primo inserimento
                else:
                    output_statement=StatementStato("Sede Accettata : È fatturabile?",s)
            else:
                output_statement=StatementStato("Sede non Accettata : Reinserire il nome della Sede",s)

        elif ( not dati["fatturabile"] and dati["sede"]) or dati["conferma"]=="fatturabile":

            negativo = ['no', 'falso','false']
            
            affermativo = ['sì', 'si', 'true', 'vero']
             
            if any(x in testo.split() for x in affermativo):
                s.addDati("fatturabile","True")
                # Se è un'operazione di modifica
                if dati["conferma"]=="fatturabile" :
                    s.addDati("conferma","non confermato")
                    output_statement=StatementStato("Fatturabilità Accettata e aggiornata. Visualizzazione Dati Aggiornati \n" + self.returnAllData(s) +" Confermare operazione di consuntivazione?",s)
                # Se è un'operazione di primo inserimento
                else:
                    output_statement=StatementStato("Scelta Fatturabilità accettata : Inserire la descrizione",s)

            elif any(x in testo.split() for x in negativo):
                s.addDati("fatturabile","False")
                # Se è un'operazione di modifica
                if dati["conferma"]=="fatturabile" :
                    s.addDati("conferma","non confermato")
                    output_statement=StatementStato("Fatturabilità Accettata e aggiornata. Visualizzazione Dati Aggiornati \n" + self.returnAllData(s) +"Confermare operazione di consuntivazione?",s)
                # Se è un'operazione di primo inserimento
                else:
                    output_statement=StatementStato("Scelta Fatturabilità accettata : Inserire la descrizione",s)
            else:
                output_statement=StatementStato("Scelta Fatturabilità non accettata : reinserire una risposta corretta ( esempio : sì/no)",s)
            
        # Utente ha inserito la sede, ora dovrà inserire la descrizione
        elif (not dati["descrizione"] and dati["fatturabile"]) or dati["conferma"]=="descrizione":
            s.addDati("descrizione",testo)
            # Se è un'operazione di modifica
            if dati["conferma"]=="descrizione" :
                s.addDati("conferma","non confermato")
                output_statement=StatementStato("Descrizione Accettata e aggiornata. Visualizzazione Dati Aggiornati \n" + self.returnAllData(s) +" Confermare operazione di consuntivazione?",s)
            # Se è un'operazione di primo inserimento
            else:
                statement = "Descrizione Accettata : Inserimento completato \n" + self.returnAllData(s) + "vuoi consuntivare? ( consuntiva per consuntivare, modifica per modificare, annulla per annullare )"
                output_statement=StatementStato(statement,s)
            
        
        # Utente ha inserito tutti i dati richiesti, ora dovrà confermare        
        elif dati:
          chiavi = ['codice progetto','data','ore fatturabili','ore viaggio','ore viaggio fatturabili','sede', 'fatturabile','descrizione']
            
          if dati["conferma"] =="modifica" :
            if any(x in testo for x in chiavi):
              s.addDati("conferma",testo)
              output_statement=StatementStato("Inserire nuovo valore per "+testo,s)
            else :
              output_statement=StatementStato("Chiave non accettata. Provare con una chiave diversa",s)
              
          else :
            annulla = ['annulla','elimina']
            modifica = ['modifica']
            consuntiva = ['sì','ok','consuntiva','procedi','conferma']        

            if any(x in testo.split() for x in consuntiva):
                s.addDati("conferma","conferma")
                Req = RequestConsuntivazione(s,Api)
                if Req.isReady():
                  if Req.sendRequest():
                      output_statement=StatementStato("Operazione avvenuta correttamente",StatoIniziale())
                  else:
                      output_statement=StatementStato("Operazione non avvenuta, riprovare? (inviare annulla per annullare)",s)
                else:
                  output_statement=StatementStato("Operazione non avvenuta correttamente, riprovare? (inviare annulla per annullare)",s)  
            
            elif any(x in testo.split() for x in annulla):
                output_statement=StatementStato("Operazione annullata",StatoIniziale())

            elif any(x in testo.split() for x in modifica):
                s.addDati("conferma","modifica")
                output_statement=StatementStato("Inserire elemento che si vuole modificare",s)
            else :
                output_statement=StatementStato("Input non valido, Reinserire",s)
            
        else:
            output_statement=StatementStato("È avvenuto un errore sconosciuto",s)

        # Aggiorno il valore di s, il cui stato sarà salvato su Client,
        # in questo modo alla prossima iterazione, il substate sarà 
        # modificato e si procederà con l'inserimento
        
        return output_statement


    def returnAllData(self,s) -> string :
        sentence =""
        values = s.getDati()
        for x in values:
            sentence += x +" : "+ values[x] + "\n"
        
        return sentence