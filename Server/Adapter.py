from decimal import InvalidOperation
from chatterbot.logic import LogicAdapter
from StatementStato import StatementStato
from StatoPresenzaSede import StatoPresenzaSede
from chatterbot.conversation import Statement
from sqlalchemy import true

class Adapter(LogicAdapter):
    """
    ---
    Class Name : Adapter 
    ---
    - Args → LogicAdapter ( type LogicAdapter) : implementata da tutti gli adapter di Chatbot
    - Description → Adapter generico da cui prendere spunto, risponde ad input "Ciao"
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
        - Description → restituisce True se l'elemento in Input contiene keyword corretta
        - Returns → boolean value : true se può eseguire, false se non può eseguire
        """
        stato=statement.getStato()
        if(statement.getText() == "ciao"):
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
        - Description → crea un outputStatement ( type StatementStato) che restituisce "Ciao, sono Bot4Me"
        - Returns → StatementStato value : risposta del chatbot
        """   
        output_statement=StatementStato("Ciao, sono Bot4Me",input_statement.getStato(),input_statement.getApiKey())
        return output_statement