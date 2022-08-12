from ast import And
from decimal import InvalidOperation
from chatterbot.logic import LogicAdapter
from RequestConsuntivazione import RequestConsuntivazione
from StatoLogin import StatoLogin
from StatementStato import StatementStato
from StatoConsuntivazione import StatoConsuntivazione
from chatterbot.conversation import Statement
from sqlalchemy import false, true
from sqlalchemy import null
from StatoIniziale import StatoIniziale

class AdapterAnnulla(LogicAdapter):
    """
    ---
    Class Name : AdapterAnnulla
    ---
    - Args → LogicAdapter ( type LogicAdapter) : implementata da tutti gli adapter di Chatbot
    - Description → Adapter utile per annullare un'operazione
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
        # Controllo su presenza stringhe che identificano la richiesta di annullamento dell'operazione
        words = ['annulla', 'termina','cancella']
        if any(x in statement.text.split() for x in words):
            return True
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
        crea un outputStatement (StatementStato) in base all'input inserito dall'utente \n
            1. Se lo stato equivale ad iniziale, non annulla nulla
            2. Altrimenti, annulla l'operazione
        - Returns → StatementStato value : risposta del chatbot
        """             
        # s rappresenta lo StatementStato
        
         # s rappresenta lo StatementStato
        if input_statement.getStato().getStatoAttuale() != StatoIniziale().getStatoAttuale() :
          output_statement=StatementStato("Operazione di "+input_statement.getStato().getStatoAttuale() +" Annullata",StatoIniziale(),null)
        elif(input_statement.getApiKey() == null):
          output_statement=StatementStato("Non Sei Loggato Non Hai Operazioni Da Annullare",StatoIniziale(),null)
        else:
          output_statement=StatementStato("Nessuna Operazione da Annullare",StatoIniziale())
        # assegno una confidence MOLTO alta per questa operazione perché DEVE prendere la priorità

        output_statement.confidence = 100

        return output_statement  