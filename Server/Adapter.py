from decimal import InvalidOperation
from chatterbot.logic import LogicAdapter
from StatementStato import StatementStato
from StatoPresenzaSede import StatoPresenzaSede
from chatterbot.conversation import Statement
from sqlalchemy import true
class Adapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        stato=statement.getStato()
        if(stato.getStatoAttuale()=="Iniziale"):
            return True
        else:
            return False

    def process(self, input_statement, additional_response_selection_parameters) -> StatementStato:
        s = input_statement.getStato()
        s.addDati("nomeSede","Bologna")
        output_statement=StatementStato("ciao",s,input_statement.getApiKey())
        return output_statement