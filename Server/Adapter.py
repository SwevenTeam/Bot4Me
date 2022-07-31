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
        if(statement.getText() == "ciao"):
            return True
        else:
            return False

    def process(self, input_statement, additional_response_selection_parameters) -> StatementStato:
        
        output_statement=StatementStato("Ciao, sono Bot4Me",input_statement.getStato(),input_statement.getApiKey())
        return output_statement