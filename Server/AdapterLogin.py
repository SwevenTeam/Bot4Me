from ast import And
from cmath import log
from decimal import InvalidOperation
from chatterbot.logic import LogicAdapter
from RequestLogin import RequestLogin
from StatementStato import StatementStato
from StatoConsuntivazione import StatoConsuntivazione
from chatterbot.conversation import Statement
from sqlalchemy import false, true
from StatoIniziale import StatoIniziale
from StatoAutenticazione import StatoAutenticazione

class AdapterLogin(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
      
      stato=statement.getStato()

      if(stato.getStatoAttuale()=="Login"):
        words = ['login', 'autenticazione','registrazione']
        if any(x in statement.text.split() for x in words):
            return True
        else:
            return False

      elif(stato.getStatoAttuale()=="Autenticazione"):
        return True

      else:
        return False

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

        s = input_statement.getStato()

        if (s.getStatoAttuale() and s.getStatoAttuale() == "Login"):
          s = StatoAutenticazione()
          output_statement=StatementStato("Autenticazione Avviata : Inserire l'API-KEY",s)

        elif(s.getStatoAttuale() == 'Autenticazione'):
          if(input_statement.getText() == '12345678-1234-1234-1234-123456789012'):
            output_statement=StatementStato("Autenticazione Avvenuta Con Successo",StatoIniziale(),input_statement.getText())
          else:
            output_statement=StatementStato("Autenticazione Fallita : l'API-KEY inserita non è valida",s)

        else:
            output_statement=StatementStato("È avvenuto un errore sconosciuto",s)
      

        return output_statement
