from ast import And
from decimal import InvalidOperation
from doctest import OutputChecker
import string
import datetime
from chatterbot.logic import LogicAdapter
from State.Statement_State import Statement_State
from chatterbot.conversation import Statement
from sqlalchemy import false, true
from State.State_Project_Creation import State_Project_Creation
from State.State_Null import State_Null
from Request.Request_Project_Creation import Request_Project_Creation
from .Util_Adapter import returnAllData, checkCodeProject, similarStringMatch, similarStringMatch_Location


class Adapter_Project_Creation(LogicAdapter):
    """
    ---
    Class Name : Adapter_Project_Creation
    ---
    - Args → LogicAdapter ( type LogicAdapter) : implementata da tutti gli adapter di Chatbot
    - Description → Adapter utilizzato per creare un nuovo progetto
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
        - Description → restituisce True se l'elemento in Input contiene keyword corretta
        - Returns → boolean value : true se può eseguire, false se non può eseguire
        """
        # Stato per fare i controlli
        state = statement.getState()

        # Se lo Stato è settato a "Iniziale", controllo se l'utente ha inserito
        # crea e progetto
        if state.getCurrentState() == "Iniziale":
            # Controllo su presenza stringhe che identificano la richiesta di
            # annullamento dell'operazione
            words = ['crea']
            words2 = ['progetto']
            if any(x in statement.text.split() for x in words) and any(
                    x in statement.text.split() for x in words2):
                return True
            else:
                return False

        # Altrimenti, controllo se lo state è creazione progetto
        elif state.getCurrentState() == "creazione progetto":
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
        - Returns → Statement_State value : risposta del chatbot
        """

        # s rappresenta lo Statement_State

        s = input_statement.getState()
        Api = input_statement.getApiKey()
        text = input_statement.getText()

        # Nel caso in cui sia settato ad "Iniziale",
        # riassegno il valore come una nuova inizializzazione di
        # StatoConsuntivazione
        if s.getCurrentState() and s.getCurrentState() == "Iniziale":
            s = State_Project_Creation()
            return Statement_State(
                "Creazione Progetto Avviata : Inserire il codice del Progetto", s)

        dati = s.getData()

        # Utente ha iniziato il processo, Adapter richiede di Inserire il codice del Progetto
        # o Utente vuole modificare il codice del progetto
        if (not dati["codice progetto"]
            ) or dati["conferma"] == "codice progetto":
            # Controllo se il progetto esiste
            if checkCodeProject(text, Api):
                s.addData("codice progetto", text)
                # Se è un'operazione di modifica
                if dati["conferma"] == "codice progetto":
                    s.addData("conferma", "non confermato")
                    output_statement = Statement_State(
                        "Codice progetto libero e dato aggiornato. Visualizzazione Dati Aggiornati \n " +
                        returnAllData(s) +
                        "Confermare operazione di creazione?",
                        s)
                # Se è un'operazione di primo inserimento
                else:
                    output_statement = Statement_State(
                        "Codice progetto libero : Inserire una descrizione", s)
            else:
                output_statement = Statement_State(
                    "Codice progetto in uso : Reinserire un codice diverso", s)

        # Utente ha inserito la sede, ora dovrà inserire la descrizione
        elif (not dati["dettagli"] and dati["codice progetto"]) or dati["conferma"] == "dettagli":
            s.addData("dettagli", text)
            # Se è un'operazione di modifica
            if dati["conferma"] == "dettagli":
                s.addData("conferma", "non confermato")
                output_statement = Statement_State(
                    "Descrizione Accettata e aggiornata. Visualizzazione Dati Aggiornati \n" +
                    returnAllData(s) +
                    " Confermare operazione di creazione?",
                    s)
            # Se è un'operazione di primo inserimento
            else:
                statement = "Descrizione Accettata : Inserire Cliente"
                output_statement = Statement_State(statement, s)

        # Utente ha inserito i dettagli, ora dovrà inserire il cliente
        elif (not dati["cliente"] and dati["dettagli"]) or dati["conferma"] == "cliente":
            s.addData("cliente", text)
            # Se è un'operazione di modifica
            if dati["conferma"] == "cliente":
                s.addData("conferma", "non confermato")
                output_statement = Statement_State(
                    "Cliente Accettato e aggiornato. Visualizzazione Dati Aggiornati \n" +
                    returnAllData(s) +
                    " Confermare operazione di creazione?",
                    s)
            # Se è un'operazione di primo inserimento
            else:
                statement = "Cliente Accettato : Inserire Manager"
                output_statement = Statement_State(statement, s)

        # Utente ha inserito il cliente, ora dovrà inserire i dettagli
        elif (not dati["manager"] and dati["cliente"]) or dati["conferma"] == "manager":
            s.addData("manager", text)
            # Se è un'operazione di modifica
            if dati["conferma"] == "manager":
                s.addData("conferma", "non confermato")
                output_statement = Statement_State(
                    "Manager Accettata e aggiornato. Visualizzazione Dati Aggiornati \n" +
                    returnAllData(s) +
                    " Confermare operazione di creazione?",
                    s)
            # Se è un'operazione di primo inserimento
            else:
                statement = "Manager Accettato : Inserire Area"
                output_statement = Statement_State(statement, s)

        # Controllo quindi se nel messaggio inviato dall'utente sia presente
        # una delle due Sedi
        elif (not dati["area"] and dati["manager"]) or dati["conferma"] == "area":
            area = similarStringMatch_Location(text.split(), Api)
            if area == '':
                output_statement = Statement_State(
                    "Area non Accettata : Reinserire il nome dell'area", s)
            else:
                s.addData("area", area)
                # Se è un'operazione di modifica
                if dati["conferma"] == "area":
                    s.addData("conferma", "non confermato")
                    output_statement = Statement_State(
                        "Area Accettata e aggiornata. Visualizzazione Dati Aggiornati \n " +
                        returnAllData(s) +
                        " Confermare operazione di creazione?",
                        s)
                # Se è un'operazione di primo inserimento
                else:
                    output_statement = Statement_State(
                        "Area Accettata : Inserire Data Inizio", s)

        # Utente ha inserito il codice e questo esiste, ora dovrà inserire la
        # data
        elif (not dati["data Inizio"] and dati["area"]) or dati["conferma"] == "data Inizio":
            # Formato aaaa-mm-gg
            try:
                datetime.datetime.strptime(text, '%Y-%m-%d')
                s.addData("data Inizio", text)
                # Se è un'operazione di modifica
                if dati["conferma"] == "data Inizio":
                    s.addData("conferma", "non confermato")
                    output_statement = Statement_State(
                        "Data di Inizio accettata e aggiornata. Visualizzazione Dati Aggiornati \n" +
                        returnAllData(s) +
                        "Confermare operazione di creazione?",
                        s)
                # Se è un'operazione di primo inserimento
                else:
                    output_statement = Statement_State(
                        "Data di Inizio accettata : Inserire la Data di Fine", s)
            except ValueError:
                output_statement = Statement_State(
                    "Data di Inizio non accettata : Reinserire la data del progetto", s)
        # Utente ha inserito il codice e questo esiste, ora dovrà inserire la
        # data
        elif (not dati["data Fine"] and dati["data Inizio"]) or dati["conferma"] == "data Fine":
            # Formato aaaa-mm-gg
            try:
                datetime.datetime.strptime(text, '%Y-%m-%d')
                s.addData("data Fine", text)
                # Se è un'operazione di modifica
                if dati["conferma"] == "data Fine":
                    s.addData("conferma", "non confermato")
                    output_statement = Statement_State(
                        "Data di Fine accettata e aggiornata. Visualizzazione Dati Aggiornati \n" +
                        returnAllData(s) +
                        "Confermare operazione di creazione?",
                        s)
                # Se è un'operazione di primo inserimento
                else:
                    output_statement = Statement_State(
                        "Data di Fine accettata : Confermare la creazione?", s)
            except ValueError:
                output_statement = Statement_State(
                    "Data di Fine non accettata : Reinserire la data del progetto", s)

        # Utente ha inserito tutti i dati richiesti, ora dovrà confermare
        elif dati:
            chiavi = [
                'codice progetto',
                'dettagli',
                'cliente',
                'manager',
                'area',
                'data Inizio',
                'data Fine', ]

            if dati["conferma"] == "modifica":
                if any(x in text for x in chiavi):
                    s.addData("conferma", text)
                    output_statement = Statement_State(
                        "Inserire nuovo valore per " + text, s)
                else:
                    output_statement = Statement_State(
                        "Chiave non accettata. Provare con una chiave diversa", s)

            else:
                annulla = ['annulla', 'elimina']
                modifica = ['modifica', 'modifica']
                consuntiva = ['sì', 'ok', 'consuntiva', 'procedi', 'conferma']

                if similarStringMatch(text.split(), consuntiva):
                    s.addData("conferma", "conferma")
                    Req = Request_Project_Creation(s, Api)
                    if Req.isReady():
                        if Req.sendRequest():
                            output_statement = Statement_State(
                                "Operazione avvenuta correttamente", State_Null())
                        else:
                            output_statement = Statement_State(
                                "Operazione non avvenuta, riprovare? (inviare annulla per annullare)", s)
                    else:
                        output_statement = Statement_State(
                            "Operazione non avvenuta correttamente, riprovare? (inviare annulla per annullare)", s)

                elif similarStringMatch(text.split(), annulla):
                    output_statement = Statement_State(
                        "Operazione annullata", State_Null())

                elif similarStringMatch(text.split(), modifica):
                    s.addData("conferma", "modifica")
                    output_statement = Statement_State(
                        "Inserire elemento che si vuole modificare", s)
                else:
                    output_statement = Statement_State(
                        "Input non valido, Reinserire", s)

        else:
            output_statement = Statement_State(
                "È avvenuto un errore sconosciuto", s)

        # Aggiorno il valore di s, il cui state sarà salvato su Client,
        # in questo modo alla prossima iterazione, il substate sarà
        # modificato e si procederà con l'inserimento

        return output_statement
