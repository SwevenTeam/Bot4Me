from ast import And
from cmath import log
from decimal import InvalidOperation
from chatterbot.logic import LogicAdapter
from State.State_Login import State_Login
from State.Statement_State import Statement_State
from chatterbot.conversation import Statement
from sqlalchemy import false, true, null
from State.State_Null import State_Null

class Adapter_Login(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
      
      state=statement.getState()

      if(state.getCurrentState()=="Iniziale"):
        words = ['login', 'autenticazione','registrazione','log','accesso']
        if any(x in statement.text.split() for x in words):
            return True
        else:
            return False

      if(state.getCurrentState()=="Login"):
        return True

      return False

    def process(self, input_statement, additional_response_selection_parameters) -> Statement_State:
      
        """
        ---
        Function Name :  process
        ---
        - Args → 
          - input_statement ( type Statement_State): frase inserita dall'utente
          - additional_response_selection_parameters ( type any): elementi extra necessari alla funzione del metodo
        - Description → 
        crea un outputStatement (Statement_State) in base all'input inserito dall'utente 
        - Returns → Statement_State value : risposta del chatbot con eventuale cambio di state
        """      

        s = input_statement.getState()

        if(input_statement.getApiKey()==null):
          if (s.getCurrentState() and s.getCurrentState() == "Iniziale"):
           s = State_Login()
           output_statement=Statement_State("Autenticazione Avviata : Inserire l'API-KEY",s)

          elif(s.getCurrentState() == 'Login'):
            if(input_statement.getText() == '12345678-1234-1234-1234-123456789012'):
              output_statement=Statement_State("Autenticazione Avvenuta Con Successo",State_Null(),input_statement.getText())
            else:
             output_statement=Statement_State("Autenticazione Fallita : l'API-KEY inserita non è valida, riprova",State_Login(),null)
        else:
            output_statement=Statement_State("Hai già effettuato l'accesso",s)
          
        return output_statement
