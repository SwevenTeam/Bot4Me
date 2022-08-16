from decimal import InvalidOperation
from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
from sqlalchemy import true
from State.Statement_State import Statement_State
from chatterbot.adapters import Adapter


class Adapter(LogicAdapter):
    """
    ---
    Class Name : Adapter
    ---
    - Args → LogicAdapter ( type LogicAdapter) : implementata da tutti gli adapter di Chatbot
    - Description → Adapter generico da cui prendere spunto, risponde ad input "Ciao"
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
        Function Name : can_process
        ---
        - Args → statement ( type Statement_State) : frase input presa dal client
        - Description → restituisce True se l'elemento in Input contiene keyword corretta
        - Returns → boolean value : true se può eseguire, false se non può eseguire
        """
        if(statement.getText() == "ciao"):
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
        - Description → crea un outputStatement ( type Statement_State) che restituisce "Ciao, sono Bot4Me"
        - Returns → Statement_State value : risposta del chatbot
        """
        output_statement = Statement_State(
            "Ciao, sono Bot4Me",
            input_statement.getState(),
            input_statement.getApiKey())
        return output_statement
