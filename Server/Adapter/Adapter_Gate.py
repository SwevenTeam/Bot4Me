from chatterbot.logic import LogicAdapter
from Request.Request_Gate import Request_Gate
from State.Statement_State import Statement_State
from State.State_Gate import State_Gate
from State.State_Null import State_Null
from .Util_Adapter import similarStringMatch_Location

class Adapter_Gate(LogicAdapter):
    """
    ---
    Class Name : Adapter_Gate
    ---
    - Args → Adapter ( type Adapter) : implementata da tutti gli adapter di Chatbot
    - Description → Adapter per l'apertura del cancello di una sede
    """

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement: Statement_State):
        """
        ---
        Function Name : can_process
        ---
        - Args → statement ( type Statement_State) : frase input presa dal client
        - Description → restituisce True se l'elemento in Input contiene keyword corretta o state uguale a cancello
        - Returns → boolean value : true se può eseguire, false se non può eseguire
        """
        state = statement.getState()

        if state.getCurrentState() == "cancello":
            return True

        if state.getCurrentState() == "Iniziale":
            words = ['cancello', 'varco', 'entrata', 'apertura', 'apri']
            return any(word in statement.text.split() for word in words)

        return False

    def process(self, input_statement: Statement_State,
                additional_response_selection_parameters) -> Statement_State:
        """
        ---
        Function Name :  process
        ---
        - Args →
          - input_statement ( type Statement_State): frase inserita dall'utente
          - additional_response_selection_parameters ( type any): elementi extra necessari alla funzione del metodo
        - Description →
        crea un outputStatement (Statement_State) in base all'input inserito dall'utente, nel caso inserisca una sede valida
        richiede l'apertura del cancello
        - Returns → Statement_State value : risposta del chatbot con eventuale cambio di state
        """
        state = input_statement.getState()
        Api = input_statement.getApiKey()
        # L'Utente vuole avviare l'attività di apertura del cancello
        if state.getCurrentState() == State_Null().getCurrentState():
            return Statement_State(
                "Apertura cancello avviata : Inserire la sede del cancello",
                State_Gate(),
                Api
            )

        Req_Gate = Request_Gate(Api)
        # vengono recuperate le sedi

        sede = ''
        similarStringMatch_Location(input_statement.text,Api)

        if sede == '':
            return Statement_State(
                "Sede non trovata : Reinserire la sede del cancello",
                state,
                Api
            )

        state.addData("sede", sede)
        Req_Gate.setSede(state)

        # viene inviata la richiesta di apertura del cancello, se non va a
        # buon fine si è verificato un errore
        if Req_Gate.isReady() and Req_Gate.sendRequest():
            return Statement_State(
                    "Sede accettata : Richiesta apertura del cancello avvenuta con successo",
                    State_Null(),
                    Api)
        else:
            return Statement_State(
                    "Sede non accettata : riprovare",
                    state,
                    Api
                )
