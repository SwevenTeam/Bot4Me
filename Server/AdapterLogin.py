from ast import And
from cmath import log
from decimal import InvalidOperation
from chatterbot.logic import LogicAdapter
from RequestLogin import RequestLogin
from StatoLogin import StatoLogin
from StatementStato import StatementStato
from StatoConsuntivazione import StatoConsuntivazione
from chatterbot.conversation import Statement
from sqlalchemy import false, true, null
from StatoIniziale import StatoIniziale

class AdapterLogin(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
      
      stato=statement.getStato()
      
      if(stato.getStatoAttuale()=="Iniziale"):
        words = ['login', 'autenticazione','registrazione','log','accesso']
        if any(x in statement.text.split() for x in words):
            return True
        else:
            return False

      if(stato.getStatoAttuale()=="Login"):
        return True

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

        if (s.getStatoAttuale() and s.getStatoAttuale() == "Iniziale" and input_statement.getApiKey()==null):
          s = StatoLogin()
          output_statement=StatementStato("Autenticazione Avviata : Inserire l'API-KEY",s)

        elif(s.getStatoAttuale() == 'Login'):
          if(input_statement.getText() == '12345678-1234-1234-1234-123456789012'):
            s = StatoIniziale()
            output_statement=StatementStato("Autenticazione Avvenuta Con Successo",s,input_statement.getText())
          else:
            output_statement=StatementStato("Autenticazione Fallita : l'API-KEY inserita non è valida, riprova",s)

        else:
            output_statement=StatementStato("Hai già effettuato l'accesso",s)
      

        return output_statement
