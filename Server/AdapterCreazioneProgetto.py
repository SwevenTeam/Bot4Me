from ast import And
from asyncio.windows_events import NULL
from decimal import InvalidOperation
from doctest import OutputChecker
import string
import datetime
from chatterbot.logic import LogicAdapter
from RequestConsuntivazione import RequestConsuntivazione
from StatementStato import StatementStato
from StatoConsuntivazione import StatoConsuntivazione
from chatterbot.conversation import Statement
from sqlalchemy import false, true
from StatoCreazioneProgetto import StatoCreazioneProgetto
from StatoIniziale import StatoIniziale
from RequestCreazioneProgetto import RequestCreazioneProgetto

class AdapterCreazioneProgetto(LogicAdapter):
    """
    ---
    Class Name : AdapterCreazioneProgetto
    ---
    - Args → LogicAdapter ( type LogicAdapter) : implementata da tutti gli adapter di Chatbot
    - Description → Adapter utilizzato per creare un nuovo progetto
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
        - Description → restituisce True se l'elemento in Input contiene keyword corretta
        - Returns → boolean value : true se può eseguire, false se non può eseguire
        """
        # Stato per fare i controlli
        stato=statement.getStato()

        # Se lo Stato è settato a "Iniziale", controllo se l'utente ha inserito crea e progetto
        if stato.getStatoAttuale() == "Iniziale":
          # Controllo su presenza stringhe che identificano la richiesta di annullamento dell'operazione
          words = ['crea']
          words2 = ['progetto']
          if any(x in statement.text.split() for x in words) and any(x in statement.text.split() for x in words2):
              return True
          else:
              return False

        # Altrimenti, controllo se lo stato è creazione progetto
        elif stato.getStatoAttuale() == "creazione progetto":
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
        - Returns → StatementStato value : risposta del chatbot
        """             
        
        # s rappresenta lo StatementStato

        s = input_statement.getStato()
        Api = input_statement.getApiKey()
        testo = input_statement.getText()
      
        # Nel caso in cui sia settato ad "Iniziale", 
        # riassegno il valore come una nuova inizializzazione di  StatoConsuntivazione
        if s.getStatoAttuale() and s.getStatoAttuale() == "Iniziale":
            s = StatoCreazioneProgetto()

        dati = s.getDati()
                    
        # Effettuo dei controlli sul Substate, per sapere cosa dover richiedere all'utente     
        if not dati["inizio"] :
        # if(s.substate =="inizio"):
            s.addDati("inizio",testo)
            output_statement=StatementStato("Creazione Progetto Avviata : Inserire il codice del Progetto",s)

        # Utente ha iniziato il processo, Adapter richiede di Inserire il codice del Progetto
        # o Utente vuole modificare il codice del progetto
        elif ( not dati["codice progetto"] and dati["inizio"] ) or dati["conferma"]=="codice progetto":
            # Controllo se il progetto esiste
            Req = RequestCreazioneProgetto(s,Api)
            if Req.checkCodeProject(testo) :
                s.addDati("codice progetto",testo)
                # Se è un'operazione di modifica
                if dati["conferma"]=="codice progetto":
                    s.addDati("conferma","non confermato")
                    output_statement=StatementStato("Codice progetto libero e dato aggiornato. Visualizzazione Dati Aggiornati \n " + self.returnAllData(s) +"Confermare operazione di creazione?",s)
                # Se è un'operazione di primo inserimento
                else:
                    output_statement=StatementStato("Codice progetto libero \n Inserire una descrizione",s)
            else :
                output_statement=StatementStato("Codice progetto in uso \n Reinserire un codice diverso",s)   
        
        # Utente ha inserito la sede, ora dovrà inserire la descrizione
        elif (not dati["dettagli"] and dati["codice progetto"]) or dati["conferma"]=="dettagli":
            s.addDati("dettagli",testo)
            # Se è un'operazione di modifica
            if dati["conferma"]=="dettagli" :
                s.addDati("conferma","non confermato")
                output_statement=StatementStato("Descrizione Accettata e aggiornata. Visualizzazione Dati Aggiornati \n" + self.returnAllData(s) +" Confermare operazione di creazione?",s)
            # Se è un'operazione di primo inserimento
            else:
                statement = "Descrizione Accettata : Inserire Cliente "
                output_statement=StatementStato(statement,s)

        # Utente ha inserito i dettagli, ora dovrà inserire il cliente
        elif (not dati["cliente"] and dati["dettagli"]) or dati["conferma"]=="cliente":
            s.addDati("cliente",testo)
            # Se è un'operazione di modifica
            if dati["conferma"]=="cliente" :
                s.addDati("conferma","non confermato")
                output_statement=StatementStato("Cliente Accettata e aggiornata. Visualizzazione Dati Aggiornati \n" + self.returnAllData(s) +" Confermare operazione di creazione?",s)
            # Se è un'operazione di primo inserimento
            else:
                statement = "Cliente Accettato : Inserire Manager "
                output_statement=StatementStato(statement,s)

        # Utente ha inserito il cliente, ora dovrà inserire i dettagli
        elif (not dati["manager"] and dati["cliente"]) or dati["conferma"]=="manager":
            s.addDati("manager",testo)
            # Se è un'operazione di modifica
            if dati["conferma"]=="manager" :
                s.addDati("conferma","non confermato")
                output_statement=StatementStato("Manager Accettata e aggiornata. Visualizzazione Dati Aggiornati \n" + self.returnAllData(s) +" Confermare operazione di creazione?",s)
            # Se è un'operazione di primo inserimento
            else:
                statement = "Manager Accettato : Inserire Area "
                output_statement=StatementStato(statement,s)


        # Controllo quindi se nel messaggio inviato dall'utente sia presente una delle due Sedi
        elif ( not dati["area"] and dati["manager"]) or dati["conferma"]=="area":
            sedeP = ['Bologna', 'bologna','bl']
            sedeI = ['Imola', 'imola', 'im']
            if any(x in testo.split() for x in sedeP):
                s.addDati("area","Bologna")
                # Se è un'operazione di modifica
                if dati["conferma"]=="area" :
                    s.addDati("conferma","non confermato")
                    output_statement=StatementStato("Area Accettata e aggiornata. Visualizzazione Dati Aggiornati \n " + self.returnAllData(s) +" Confermare operazione di creazione?",s)
                # Se è un'operazione di primo inserimento
                else:
                    output_statement=StatementStato("Area Accettata : Inserire Data Inizio",s)
            elif any(x in testo.split() for x in sedeI):
                s.addDati("area","Imola")
                # Se è un'operazione di modifica
                if dati["conferma"]=="area" :
                    s.addDati("conferma","non confermato")
                    output_statement=StatementStato("Area Accettata e aggiornata. Visualizzazione Dati Aggiornati \n " + self.returnAllData(s) +" Confermare operazione di creazione?",s)
                # Se è un'operazione di primo inserimento
                else:
                    output_statement=StatementStato("Area Accettata : Inserire Data Inizio",s)
            else:
                output_statement=StatementStato("Area non Accettata : Reinserire il nome dell'area",s)

            
        # Utente ha inserito il codice e questo esiste, ora dovrà inserire la data
        elif (not dati["data Inizio"] and dati["area"] ) or dati["conferma"]=="data Inizio":
            ### Formato aaaa-mm-gg
            try:
                datetime.datetime.strptime(testo, '%Y-%m-%d')
                s.addDati("data Inizio",testo)
                # Se è un'operazione di modifica
                if dati["conferma"]=="data":
                    s.addDati("conferma","non confermato")
                    output_statement=StatementStato("Data di Inizio accettata e aggiornata. Visualizzazione Dati Aggiornati \n" + self.returnAllData(s) +"Confermare operazione di creazione?",s)
                # Se è un'operazione di primo inserimento
                else:
                    output_statement=StatementStato("Data di Inizio accettata : Inserire la Data di Fine",s)
            except ValueError:
                output_statement=StatementStato("Data di Inizio non accettata : Reinserire la data del progetto",s)
        # Utente ha inserito il codice e questo esiste, ora dovrà inserire la data
        elif (not dati["data Fine"] and dati["data Inizio"] ) or dati["conferma"]=="data Fine":
            ### Formato aaaa-mm-gg
            try:
                datetime.datetime.strptime(testo, '%Y-%m-%d')
                s.addDati("data Fine",testo)
                # Se è un'operazione di modifica
                if dati["conferma"]=="data":
                    s.addDati("conferma","non confermato")
                    output_statement=StatementStato("Data di Fine accettata e aggiornata. Visualizzazione Dati Aggiornati \n" + self.returnAllData(s) +"Confermare operazione di creazione?",s)
                # Se è un'operazione di primo inserimento
                else:
                    output_statement=StatementStato("Data di Fine accettata : Confermare la creazione?",s)
            except ValueError:
                output_statement=StatementStato("Data di Fine non accettata : Reinserire la data del progetto",s)
        
        
        # Utente ha inserito tutti i dati richiesti, ora dovrà confermare        
        elif dati:
          chiavi = ['inizio','codice progetto','dettagli','cliente','manager','status','area','data Inizio','date Fine']
            
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
                Req = RequestCreazioneProgetto(s,Api)
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