from ast import And
from asyncio.windows_events import NULL
from decimal import InvalidOperation
from chatterbot.logic import LogicAdapter
from RequestConsuntivazione import RequestConsuntivazione
from StatementStato import StatementStato
from StatoConsuntivazione import StatoConsuntivazione
from sqlalchemy import false, null, true
from StatoIniziale import StatoIniziale

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

        # Nel caso in cui sia settato ad "Iniziale", 
        # riassegno il valore come una nuova inizializzazione di  StatoConsuntivazione
        if s.getStatoAttuale() and s.getStatoAttuale() == "Iniziale":
            s = StatoConsuntivazione()

        # Effettuo dei controlli sul Substate, per sapere cosa dover richiedere all'utente        
        if(s.substate =="inizio"):
            output_statement=StatementStato("Consuntivazione Avviata : Inserire il nome della sede",s)
            s.aggiornamento(input_statement)

        # Utente ha iniziato il processo, Adapter richiede di Inserire la Sede
        # Controllo quindi se nel messaggio inviato dall'utente sia presente una delle due Sedi
        elif(s.substate =="Sede"):
            sedeP = ['Bologna', 'bologna','bl']
            
            sedeI = ['Imola', 'imola', 'im']
             
            if any(x in input_statement.text.split() for x in sedeP):
              output_statement=StatementStato("Sede Accettata : Inserire la descrizione del progetto",s)
              s.aggiornamento(StatementStato("Bologna",s) )
            elif any(x in input_statement.text.split() for x in sedeI):
              output_statement=StatementStato("Sede Accettata : Inserire la descrizione del progetto",s)
              s.aggiornamento(StatementStato("Imola",s))
            else:
              output_statement=StatementStato("Sede non Accettata : Reinserire il nome della Sede",s)

        # Utente ha inserito la sede, ora dovrà inserire la descrizione
        elif(s.substate =="descrizione"):
            output_statement=StatementStato("Descrizione Accettata : Inserire la data del progetto (formato aaaa-mm-gg)",s)
            s.aggiornamento(input_statement)

        # Utente ha inserito la descrizione, ora dovrà inserire la data
        elif(s.substate =="data"):
            ### Da sistemare quando conosco il formato della data
            if True :
              output_statement=StatementStato("Data Accettata : Inserire la durata del progetto",s)
              s.aggiornamento(input_statement)
            else:
              output_statement=StatementStato("Data non Accettata : Reinserire la data del progetto",s)
              
        # Utente ha inserito la data, ora dovrà inserire la durata
        elif(s.substate =="durata"):
            s.aggiornamento(input_statement)
            values = s.getDati()
            stringa = "Durata Accettata; \n Dati Inseriti : \n"
            for x in values:
              stringa += x +" : "+ values[x] + "\n"
            stringa += " Confermare l'operazione?"
            
            output_statement=StatementStato(stringa,s)
        
        # Utente ha inserito tutti i dati richiesti, ora dovrà confermare        
        elif(s.substate =="termina"):
          annulla = ['no', 'annulla','elimina']
          if not any(x in input_statement.text.split() for x in annulla):
              Req = RequestConsuntivazione(s,input_statement.getApiKey())
              if Req.isReady():
                if Req.sendRequest():
                    output_statement=StatementStato("Operazione avvenuta correttamente",StatoIniziale())
                else:
                    output_statement=StatementStato("Operazione non avvenuta, riprovare? (inviare annulla per annullare)",s)
              else:
                output_statement=StatementStato("Operazione non avvenuta correttamente, riprovare? (inviare annulla per annullare)",s)     
          else:
              output_statement=null
              output_statement.confidence = 0
        else:
            output_statement=StatementStato("È avvenuto un errore sconosciuto",s)

        # Aggiorno il valore di s, il cui stato sarà salvato su Client,
        # in questo modo alla prossima iterazione, il substate sarà 
        # modificato e si procederà con l'inserimento
        
        return output_statement
