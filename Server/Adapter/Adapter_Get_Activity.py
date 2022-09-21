from ast import And
from decimal import InvalidOperation
import string
from chatterbot.logic import LogicAdapter
from Request.Request_Get_Activity import Request_Get_Activity
from State.Statement_State import Statement_State
from State.State_Get_Activity import State_Get_Activity
from sqlalchemy import false, null, true
from State.State_Null import State_Null
import datetime
from datetime import date
from .Util_Adapter import returnAllData, checkProjectExistance, similarStringMatch, similarStringMatch_Location


class Adapter_Get_Activity(LogicAdapter):
    """
    ---
    Class Name : Adapter_Activity
    ---
    - Args → LogicAdapter ( type LogicAdapter) : implementata da tutti gli adapter di Chatbot
    - Description → Adapter utilizzato per effettuare una consuntivazione
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
        Function Name :  can_process
        ---
        - Args → statement ( type Statement_State) : frase input presa dal client
        - Description → restituisce True se l'elemento in Input contiene keyword corretta o state uguale a Consuntivazione
        - Returns → boolean value : true se può eseguire, false se non può eseguire
        """
        # Stato per fare i controlli
        state = statement.getState()

        if statement.getApiKey() == null:
            return False

        # Se lo Stato è settato a "Iniziale", controllo se l'utente ha inserito
        # consuntivo
        if state.getCurrentState() == "Iniziale":

            # Controllo su presenza stringhe che identificano la richiesta di
            # consuntivazione
            words1 = [
                'ottieni',
                'get',
                'restituire',
                'restituisci',
                'ritorna']
            words2 = [
                'consuntivazione',
                'consuntivare',
                'con',
                'consuntiva',
                'consuntivo']
            return similarStringMatch(
                statement.text.split(),
                words1) and similarStringMatch(
                statement.text.split(),
                words2)

        elif state.getCurrentState() == "restituzione consuntivazione":
            return True
        # Infine, se nessuno dei due if restituiscono vero, questo adapter non
        # potrà effettuare il process
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
        - Description →
        crea un outputStatement (Statement_State) in base all'input inserito dall'utente
        - Returns → Statement_State value : risposta del chatbot con eventuale cambio di state
        """
        # s rappresenta lo Statement_State
        s = input_statement.getState()
        Api = input_statement.getApiKey()
        text = input_statement.getText()
        data = s.getData()

        if s.getCurrentState() and s.getCurrentState() == "Iniziale":
            s = State_Get_Activity()
            output_statement = Statement_State(
                "Operazione Restituzione di Consuntivazione Avviata : Inserire la data da cui iniziare a visualizzare", s)
        elif s.getCurrentState() == "restituzione consuntivazione" :
            if not data["data"] :
                if similarStringMatch("oggi",text) :
                    s.addData("data",  date.today().strftime('%Y-%m-%d'))
                    output_statement = Statement_State(
                        "Data accettata : Inserire il codice del Progetto", s)
                else :
                    try:
                        datetime.datetime.strptime(text, '%Y-%m-%d')
                        s.addData("data", text)

                        output_statement = Statement_State(
                            "Data accettata : Inserire il codice del Progetto", s)
                    except ValueError:
                        output_statement = Statement_State(
                            "Data non accettata : Reinserire la data del progetto", s)
            elif data["data"] and not data["codice progetto"] :
                if text.isnumeric():
                    if checkProjectExistance(text, Api):
                        s.addData("codice progetto", text)
                        Req = Request_Get_Activity(s, Api)
                        if Req.isReady():
                            result = Req.sendRequest()
                            if result == []:
                                output_statement = Statement_State(
                                    "Nessun elemento da visualizzare", State_Null(), Api)
                            else:
                                output_statement = Statement_State(
                                    result, State_Null(), Api)
                        else:
                            output_statement = Statement_State(
                                "Sembra che tu debba ancora Inserire il codice", s)
                    else:
                        output_statement = Statement_State(
                            "Progetto Inesistente : Inserire un nuovo codice", s)

                else:
                    output_statement = Statement_State(
                        "Inserire il codice del Progetto come numero", s)
        else :
            output_statement = Statement_State(
                    "È avvenuto un errore, provare a reinserire", s)

        output_statement.confidence = 0.8
        return output_statement
