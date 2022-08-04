from ast import And
from decimal import InvalidOperation
from chatterbot.logic import LogicAdapter
from RequestLogin import RequestLogin
from StatementStato import StatementStato
from StatoConsuntivazione import StatoConsuntivazione
from chatterbot.conversation import Statement
from sqlalchemy import false, true
from StatoIniziale import StatoIniziale

class AdapterLogin(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        words = ['login', 'autenticazione','registrazione']
        if any(x in statement.text.split() for x in words):
            return True
        else:
            return False

    def process(self, input_statement, additional_response_selection_parameters) -> StatementStato:
        
        # s rappresenta lo StatementStato
        if input_statement.getStato().getStatoAttuale() != StatoIniziale().getStatoAttuale() :
          output_statement=StatementStato("Operazione di Login avvenuta Correttamente",StatoIniziale())
        else:
          output_statement=StatementStato("Operazione di Login non avvenuta",StatoIniziale())
        return output_statement
