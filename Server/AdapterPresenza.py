from decimal import InvalidOperation
from chatterbot.logic import LogicAdapter
from StatementStato import StatementStato
from StatoPresenzaSede import StatoPresenzaSede
from RequestPresenza import RequestPresenza
from StatoIniziale import StatoIniziale
from chatterbot.conversation import Statement
from sqlalchemy import true


class AdapterPresenza(LogicAdapter):
    """
    ---
    Class Name : AdapterPresenza 
    ---
    - Args → LogicAdapter ( type LogicAdapter) : implementata da tutti gli adapter di Chatbot
    - Description → Adapter utile per registrare la presenza in una sede
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
        Function Name : can_process
        ---
        - Args → statement ( type StatementStato) : frase input presa dal client
        - Description → restituisce True se l'elemento in Input contiene keyword corretta o stato uguale a presenza sede
        - Returns → boolean value : true se può eseguire, false se non può eseguire
        """
        # Stato per fare i controlli
        stato=statement.getStato()

        # Se lo Stato è settato a "Iniziale", controllo se l'utente ha inserito consuntivo        
        if stato.getStatoAttuale()=="Iniziale":

            # Controllo su presenza stringhe che identificano la richiesta di presenza
            words = ['presenza', 'presenze']
            if any(x in statement.text.split() for x in words):
              return True
            else :
              return False

        # Altrimenti, controllo se lo stato è presenza sede
        elif stato.getStatoAttuale()=="presenza Sede":
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
        crea un outputStatement (StatementStato) in base all'input inserito dall'utente, nel caso in cui tutti i dati siano presenti, registra la presenza
        - Returns → StatementStato value : risposta del chatbot con eventuale cambio di stato
        """ 

        # s rappresenta lo StatementStato
        s = input_statement.getStato()

        # Nel caso in cui sia settato ad "Iniziale", 
        # riassegno il valore come una nuova inizializzazione di  StatoPresenza
        if s.getStatoAttuale() and s.getStatoAttuale() == "Iniziale":
            s = StatoPresenzaSede()
            output_statement=StatementStato("Operazione di registrazione della presenza avviata : inserire il nome di una sede",s,input_statement.getApiKey())
        else:
            sedeP = ['Bologna', 'bologna','bl']
            
            sedeI = ['Imola', 'imola', 'im']
             
            if any(x in input_statement.text.split() for x in sedeP):
                s.addNomeSede("Bologna")
                output_statement= self.callRequest(input_statement)
            elif any(x in input_statement.text.split() for x in sedeI):
                s.addNomeSede("Imola")
                output_statement= self.callRequest(input_statement)
            else:
                output_statement=StatementStato("Sede non Accettata : Reinserire il nome della Sede",s)
            
        return output_statement


    ### callRequest
    ### input : self, frase input presa dal client
    ### output : StatementStato, varia in base al risultato della Request
    def callRequest(self, input_statement) -> StatementStato :
        """
        ---
        Function Name : callRequest
        ---
        - Args → input_statement (StatementStato): frase inserita dall'utente
        - Description → 
            - richiama isReady() su RequestPresenza; 
            - se quest ultimo restituisce true potrà effettuare la richiesta; 
            - invia la richiesta e restituisce il valore associato 
        - Returns → StatementStato: risposta del chatbot con eventuale cambio di stato
        """
        Req = RequestPresenza(input_statement.getStato(),input_statement.getApiKey())
        if Req.isReady():
            if Req.sendRequest():
                output_statement=StatementStato("Registrazione presenza effettuata con Successo",StatoIniziale())
            else:
                output_statement=StatementStato("Registrazione presenza Fallita",StatoIniziale())      
        else:
            output_statement=StatementStato("Request non pronto a soddisfare la richiesta",input_statement.getStato())
        return output_statement