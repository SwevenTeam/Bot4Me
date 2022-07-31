from decimal import InvalidOperation
from chatterbot.logic import LogicAdapter
from StatementStato import StatementStato
from StatoPresenzaSede import StatoPresenzaSede
from RequestPresenza import RequestPresenza
from StatoIniziale import StatoIniziale
from chatterbot.conversation import Statement
from sqlalchemy import true
class AdapterPresenza(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        stato=statement.getStato()
        if stato.getStatoAttuale()=="Iniziale":
            words = ['presenza', 'presenze']
            if any(x in statement.text.split() for x in words):
              return True
            else :
              return False
        elif stato.getStatoAttuale()=="presenza Sede":
            return True
        else:
            return False

    def process(self, input_statement, additional_response_selection_parameters) -> StatementStato:
        
        s = input_statement.getStato()

        # Nel caso in cui sia settato ad "Iniziale", 
        # riassegno il valore come una nuova inizializzazione di  StatoPresenza
        if s.getStatoAttuale() and s.getStatoAttuale() == "Iniziale":
            s = StatoPresenzaSede()
            output_statement=StatementStato("Operazione di registrazione della presenza avviata : inserire il nome di una sede",s,input_statement.getApiKey())
        else:
            sedeP = ['Bologna', 'bologna','bl']
            
            sedeI = ['Imola', 'imola', 'im']
             
            if any(x in input_statement.text.split() for x in sedeP):
                s.addNomeSede("Bologna")
                output_statement= self.callRequest(input_statement)
            elif any(x in input_statement.text.split() for x in sedeI):
                s.addNomeSede("Imola")
                output_statement= self.callRequest(input_statement)
            else:
                output_statement=StatementStato("Sede non Accettata : Reinserire il nome della Sede",s)
            
        return output_statement

    def callRequest(self, input_statement) -> StatementStato :

        Req = RequestPresenza(input_statement.getStato(),input_statement.getApiKey())
        if Req.isReady():
            if Req.sendRequest():
                output_statement=StatementStato("Registrazione presenza effettuata con Successo",StatoIniziale())
            else:
                output_statement=StatementStato("Registrazione presenza Fallita",StatoIniziale())      
        else:
            output_statement=StatementStato("Request non pronto a soddisfare la richiesta",input_statement.getStato())
        return output_statement