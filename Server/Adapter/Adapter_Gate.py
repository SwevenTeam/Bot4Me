from chatterbot.logic import LogicAdapter
from Server.Request.Request_Gate import Request_Gate
from Server.State.Statement_State import Statement_State
from Server.State.State_Gate import State_Gate
from Server.State.State_Null import State_Null
from .Util_Adapter import getLocationList, similarStringMatch_Location, similarStringMatch


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
        if statement.getApiKey() == '':
            return False

        state = statement.getState()

        if state.getCurrentState() == "cancello":
            return True

        if state.getCurrentState() == "Iniziale":
            words = ['cancello', 'varco', 'entrata', 'apertura', 'apri']
            return similarStringMatch(statement.text.split(), words)

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
        text = input_statement.getText()

        # L'Utente vuole avviare l'attività di apertura del cancello
        if state.getCurrentState() == State_Null().getCurrentState():
            output_statement = Statement_State(
                "Apertura cancello avviata : Inserire la sede del cancello",
                State_Gate(),
                Api
            )

        # L'utente ha già avviato la procedura e deve inserire la sede
        elif state.getData()['sede'] == '':
            location = similarStringMatch_Location(text.split(), Api)
            if location == '':
                output_statement = Statement_State(
                    "Sede non trovata : Reinserire la sede del cancello",
                    state,
                    Api
                )
            else:
                state.addData("sede", location)
                output_statement = Statement_State(
                    f"Sede accettata : Confermare l'apertura del cancello della sede di {state.getData()['sede']}? (si, modifica, annulla)",
                    state,
                    Api
                )
        else:
            # controllo se l'utente vuole modificare la sede
            modifica = ['cambia', 'modifica', ]
            conferma = ['si', 'sì', 'ok', 'apri', 'procedi', 'conferma']
            if similarStringMatch(text.split(), modifica):
                # viene fatto il reset della sede
                state.addData('sede', '')
                output_statement = Statement_State(
                    "Modifica della sede : Inserire la sede del cancello",
                    state,
                    Api
                )

            elif similarStringMatch(text.split(), conferma):
                request_cancello = Request_Gate(state, Api)

                # viene inviata la richiesta di apertura del cancello, se non
                # va a buon fine si è verificato un errore
                if request_cancello.isReady():
                    if request_cancello.sendRequest():
                        output_statement = Statement_State(
                            "Sede accettata : Richiesta apertura del cancello avvenuta con successo",
                            State_Null(),
                            Api
                        )
                    else:
                        output_statement = Statement_State(
                            "Si è verificato un errore sconosciuto, riprova a confermare", state, Api)
                else:
                    output_statement = Statement_State(
                        "Dati non inseriti correttamente, provare a modificare e reinserire", state, Api)

            else:
                output_statement = Statement_State(
                    "Confermare l'apertura del cancello della sede di " +
                    state.getData()['sede'] +
                    "? (si, modifica annulla)",
                    state,
                    Api)

        return output_statement
