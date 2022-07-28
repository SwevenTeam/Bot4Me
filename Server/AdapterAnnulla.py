from ast import And
from asyncio.windows_events import NULL
from decimal import InvalidOperation
from chatterbot.logic import LogicAdapter
from RequestConsuntivazione import RequestConsuntivazione
from StatementStato import StatementStato
from StatoConsuntivazione import StatoConsuntivazione
from chatterbot.conversation import Statement
from sqlalchemy import false, true
from StatoIniziale import StatoIniziale

class AdapterAnnulla(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        words = ['annulla', 'termina','cancella']
        if any(x in statement.text.split() for x in words):
            return True
        else:
            return False

    def process(self, input_statement, additional_response_selection_parameters) -> StatementStato:
        
        # s rappresenta lo StatementStato
        if input_statement.getStato().getStatoAttuale() != StatoIniziale().getStatoAttuale() :
          output_statement=StatementStato("Operazione di "+input_statement.getStato().getStatoAttuale() +" Annullata",StatoIniziale())
        else:
          output_statement=StatementStato("Nessuna Operazione da Annullare",StatoIniziale())
        output_statement.confidence = 100
        return output_statement
