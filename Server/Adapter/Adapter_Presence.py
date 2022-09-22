from decimal import InvalidOperation
from chatterbot.logic import LogicAdapter
from State.Statement_State import Statement_State
from State.State_Presence import State_Presence
from Request.Request_Presence import Request_Presence
from State.State_Null import State_Null
from chatterbot.conversation import Statement
from sqlalchemy import true
from .Util_Adapter import checkPresence, similarStringMatch, similarStringMatch_Location


class Adapter_Presence(LogicAdapter):
    """
    ---
    Class Name : Adapter_Presence
    ---
    - Args → LogicAdapter ( type LogicAdapter) : implementata da tutti gli adapter di Chatbot
    - Description → Adapter utile per registrare la presenza in una sede
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
        Function Name : can_process
        ---
        - Args → statement ( type Statement_State) : frase input presa dal client
        - Description → restituisce True se l'elemento in Input contiene keyword corretta o state uguale a presenza sede
        - Returns → boolean value : true se può eseguire, false se non può eseguire
        """
        # Stato per fare i controlli
        state = statement.getState()

        # Se lo Stato è settato a "Iniziale", controllo se l'utente ha inserito
        # consuntivo
        if state.getCurrentState() == "Iniziale":

            # Controllo su presenza stringhe che identificano la richiesta di
            # presenza o di checkout
            words = ['presenza', 'presenze','checkin','checkout','check-out','esci']
            return similarStringMatch(statement.text.split(), words)

        # Altrimenti, controllo se lo state è presenza sede
        elif state.getCurrentState() == "presenza Sede":
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
        crea un outputStatement (Statement_State) in base all'input inserito dall'utente, nel caso in cui tutti i dati siano presenti, registra la presenza
        - Returns → Statement_State value : risposta del chatbot con eventuale cambio di state
        """

        # s rappresenta lo Statement_State
        s = input_statement.getState()
        text = input_statement.text.split()
        Api = input_statement.getApiKey()
        # Parole Chiave per Check Out
        checkout = ['checkout','check-out','esci']
        # Nel caso in cui sia settato ad "Iniziale",
        # riassegno il valore come una nuova inizializzazione di  StatoPresenza
        if s.getCurrentState() and s.getCurrentState() == "Iniziale":
            # Controllo se si vuole effettuare un Check In o un Check Out
            
            if similarStringMatch(text,checkout) :
                place = checkPresence(Api)
                if place == '' :
                    output_statement = Statement_State(
                        "Impossibile effetuare il Check Out senza prima effettuare una registrazione",
                        s,
                        Api)
                else:
                    s = State_Presence()
                    s.addData("sede", place)
                    Req = Request_Presence(
                        s,
                        Api)
                    if Req.isReady():
                        if Req.sendRequest(False):
                            output_statement = Statement_State(
                            "Check Out effettuato con successo",
                            State_Null(),
                            Api)
                        else :
                            output_statement = Statement_State(
                            "È avvenuto un errore nella richiesta, riprovare ",
                            input_statement.getState(),
                            Api)
                    else :
                        output_statement = Statement_State(
                          "Request non pronto a soddisfare la richiesta",
                          input_statement.getState(),
                          Api)

            else :
                answer = "Hai già registrato una presenza, inserire una nuove sede per effettuare un'altra registrazione (annulla per annullare)" if checkPresence(Api) else "Operazione di registrazione della presenza avviata : inserire il nome di una sede"
                s = State_Presence()
                output_statement = Statement_State(
                    answer,
                    s,
                    Api)
        else:
            sedi = similarStringMatch_Location(text, Api)
            if sedi == '':
                output_statement = Statement_State(
                    "Sede non Accettata : Reinserire il nome della Sede", s)
            else:
                s.addData("sede", sedi)
                
                Req = Request_Presence(
                    input_statement.getState(),
                    Api)
                if Req.isReady():
                    if Req.sendRequest():
                        output_statement = Statement_State(
                            "Registrazione presenza effettuata con Successo", State_Null(), Api)
                    else:
                        output_statement = Statement_State(
                            "Registrazione presenza Fallita", s)
                else:
                    output_statement = Statement_State(
                        "Request non pronto a soddisfare la richiesta",
                        input_statement.getState())

        return output_statement
