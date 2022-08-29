
from chatterbot.logic import LogicAdapter
from Server.State.Statement_State import Statement_State
from chatterbot.conversation import Statement
from sqlalchemy import false, true
from sqlalchemy import null
from Server.State.State_Null import State_Null


class Adapter_Undo(LogicAdapter):
    """
    ---
    Class Name : Adapter_Undo
    ---
    - Args → LogicAdapter ( type LogicAdapter) : implementata da tutti gli adapter di Chatbot
    - Description → Adapter utile per annullare un'operazione
    """
    # Costruttore

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    # can_process
    # input : self, frase input presa dal client
    # output : boolean, true se può eseguire, false se non può eseguire

    def can_process(self, statement):
        """
        ---
        Function Name :  can_process
        ---
        - Args → statement ( type Statement_State) : frase input presa dal client
        - Description → restituisce True se l'elemento in Input contiene keyword corretta
        - Returns → boolean value : true se può eseguire, false se non può eseguire
        """
        # Controllo su presenza stringhe che identificano la richiesta di
        # annullamento dell'operazione
        words = ['annulla', 'termina', 'cancella']
        if any(x in statement.text.split() for x in words):
            return True
        else:
            return False

    # process
    # input : self, frase input presa dal client, ( eventuali info extra )
    # output : Statement_State, varia in base a quale operazione si sta
    # eseguendo

    def process(
            self,
            input_statement,
            additional_response_selection_parameters) -> Statement_State:
        """
        ---
        Function Name :  process
        ---
        - Args →
          - input_statement ( type Statement_State): frase inserita dall'utente
          - additional_response_selection_parameters ( type any): elementi extra necessari alla funzione del metodo
        - Description →
        crea un outputStatement (Statement_State) in base all'input inserito dall'utente \n
            1. Se lo state equivale ad iniziale, non annulla nulla
            2. Altrimenti, annulla l'operazione
        - Returns → Statement_State value : risposta del chatbot
        """
        # s rappresenta lo Statement_State

        # s rappresenta lo Statement_State
        if input_statement.getState().getCurrentState() != State_Null().getCurrentState():
            output_statement = Statement_State(
                "Operazione di " +
                input_statement.getState().getCurrentState() +
                " Annullata",
                State_Null(),
                input_statement.getApiKey()
            )
        elif(input_statement.getApiKey() == null):
            output_statement = Statement_State(
                "Non Sei Loggato e non Hai Operazioni Da Annullare", State_Null(), null)
        else:
            output_statement = Statement_State(
                "Nessuna Operazione da Annullare", State_Null())
        # assegno una confidence MOLTO alta per questa operazione perché DEVE
        # prendere la priorità

        output_statement.confidence = 0.9

        return output_statement
