from ast import And
from decimal import InvalidOperation
import string
from chatterbot.logic import LogicAdapter
from Request.Request_Activity import Request_Activity
from State.Statement_State import Statement_State
from State.State_Activity import State_Activity
from sqlalchemy import false, null, true
from State.State_Null import State_Null
import datetime
from .Util_Adapter import returnAllData, checkProjectExistance, similarStringMatch, similarStringMatch_Location


class Adapter_Activity(LogicAdapter):
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
            words = [
                'consuntivazione',
                'consuntivare',
                'con',
                'consuntiva',
                'consuntivo']
            return similarStringMatch(statement.text.split(), words)

        # Altrimenti, controllo se lo state è consuntivazione
        elif state.getCurrentState() == "consuntivazione":
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

        # Nel caso in cui sia settato ad "Iniziale",
        # riassegno il valore come una nuova inizializzazione di
        # StatoConsuntivazione
        if s.getCurrentState() and s.getCurrentState() == "Iniziale":
            s = State_Activity()
            return Statement_State(
                "Consuntivazione Avviata : Inserire il codice del Progetto", s)

        dati = s.getData()

        # Utente ha iniziato il processo, Adapter richiede di Inserire il codice del Progetto
        # o Utente vuole modificare il codice del progetto
        if (not dati["codice progetto"]
                ) or dati["conferma"] == "codice progetto":
            # Controllo se il progetto esiste
            if checkProjectExistance(text, Api):
                s.addData("codice progetto", text)
                # Se è un'operazione di modifica
                if dati["conferma"] == "codice progetto":
                    s.addData("conferma", "non confermato")
                    output_statement = Statement_State(
                        "Progetto esistente e dato aggiornato. Visualizzazione Dati Aggiornati <br> " +
                        returnAllData(s) +
                        "Confermare operazione di consuntivazione?",
                        s)
                # Se è un'operazione di primo inserimento
                else:
                    output_statement = Statement_State(
                        "Progetto esistente : Inserire la data di consuntivazione ( formato aaaa-mm-gg )", s)
            else:
                output_statement = Statement_State(
                    "Progetto non esistente : Reinserire un codice diverso o creare un nuovo progetto", s)

        # Utente ha inserito il codice e questo esiste, ora dovrà inserire la
        # data
        elif (not dati["data"] and dati["codice progetto"]) or dati["conferma"] == "data":
            # Formato aaaa-mm-gg
            try:
                datetime.datetime.strptime(text, '%Y-%m-%d')
                s.addData("data", text)
                # Se è un'operazione di modifica
                if dati["conferma"] == "data":
                    s.addData("conferma", "non confermato")
                    output_statement = Statement_State(
                        "Data accettata e aggiornata. Visualizzazione Dati Aggiornati <br>" +
                        returnAllData(s) +
                        "Confermare operazione di consuntivazione?",
                        s)
                # Se è un'operazione di primo inserimento
                else:
                    output_statement = Statement_State(
                        "Data accettata : Inserire le ore fatturabili", s)
            except ValueError:
                output_statement = Statement_State(
                    "Data non accettata : Reinserire la data del progetto", s)

        # Utente ha inserito la data nel formato corretto, ora dovrà inserire
        # le ore fatturabili
        elif (not dati["ore fatturabili"] and dati["data"]) or dati["conferma"] == "ore fatturabili":
            if text.isnumeric():
                s.addData("ore fatturabili", text)
                # Se è un'operazione di modifica
                if dati["conferma"] == "ore fatturabili":
                    s.addData("conferma", "non confermato")
                    output_statement = Statement_State(
                        "Ore Fatturabili accettate e aggiornate. Visualizzazione Dati Aggiornati <br>" +
                        returnAllData(s) +
                        "Confermare operazione di consuntivazione?",
                        s)
                # Se è un'operazione di primo inserimento
                else:
                    output_statement = Statement_State(
                        "Ore fatturabili accettate : Inserire le ore di viaggio", s)
            else:
                output_statement = Statement_State(
                    "Ore fatturabili non accettate : Reinserire le ore fatturabili come numero", s)

        # Utente ha inserito il codice e questo esiste, ora dovrà inserire la
        # data
        elif (not dati["ore viaggio"] and dati["ore fatturabili"]) or dati["conferma"] == "ore viaggio":
            if text.isnumeric():
                s.addData("ore viaggio", text)
                # Se è un'operazione di modifica
                if dati["conferma"] == "ore viaggio":
                    s.addData("conferma", "non confermato")
                    output_statement = Statement_State(
                        "Ore di viaggio accettate e aggiornate. Visualizzazione Dati Aggiornati " +
                        returnAllData(s) +
                        "Confermare operazione di consuntivazione?",
                        s)
                # Se è un'operazione di primo inserimento
                else:
                    output_statement = Statement_State(
                        "Ore viaggio accettate : Inserire le ore di viaggio fatturabili", s)
            else:
                output_statement = Statement_State(
                    "Ore viaggio non accettate : Reinserire le ore di viaggio come numero", s)

        # Utente ha inserito il codice e questo esiste, ora dovrà inserire la
        # data
        elif (not dati["ore viaggio fatturabili"] and dati["ore viaggio"]) or dati["conferma"] == "ore viaggio fatturabili":
            if text.isnumeric():
                s.addData("ore viaggio fatturabili", text)
                # Se è un'operazione di modifica
                if dati["conferma"] == "ore viaggio":
                    s.addData("conferma", "non confermato")
                    output_statement = Statement_State(
                        "Ore di viaggio fatturabili accettate e aggiornate. Visualizzazione Dati Aggiornati " +
                        returnAllData(s) +
                        " Confermare operazione di consuntivazione?",
                        s)
                # Se è un'operazione di primo inserimento
                else:
                    output_statement = Statement_State(
                        "Ore viaggio fatturabili Accettate : Inserire la sede", s)
            else:
                output_statement = Statement_State(
                    "Ore viaggio fatturabili non accettate : Reinserire le ore di viaggio fatturabili come numero", s)

        # Controllo quindi se nel messaggio inviato dall'utente sia presente
        # una delle due Sedi
        elif (not dati["sede"] and dati["ore viaggio fatturabili"]) or dati["conferma"] == "sede":
            sedi = similarStringMatch_Location(text, Api)
            if sedi == '':
                output_statement = Statement_State(
                    "Sede non Accettata : Reinserire il nome della Sede", s)
            else:
                s.addData("sede", sedi)
                # Se è un'operazione di modifica
                if dati["conferma"] == "sede":
                    s.addData("conferma", "non confermato")
                    output_statement = Statement_State(
                        "Sede Accettata e aggiornata. Visualizzazione Dati Aggiornati <br> " +
                        returnAllData(s) +
                        " Confermare operazione di consuntivazione?",
                        s)
                # Se è un'operazione di primo inserimento
                else:
                    output_statement = Statement_State(
                        "Sede Accettata : È fatturabile?", s)
        elif (not dati["fatturabile"] and dati["sede"]) or dati["conferma"] == "fatturabile":

            negativo = ['no', 'falso', 'false']

            affermativo = ['sì', 'si', 'true', 'vero']

            if any(x in text.split() for x in affermativo):
                s.addData("fatturabile", "True")
                # Se è un'operazione di modifica
                if dati["conferma"] == "fatturabile":
                    s.addData("conferma", "non confermato")
                    output_statement = Statement_State(
                        "Fatturabilità Accettata e aggiornata. Visualizzazione Dati Aggiornati <br>" +
                        returnAllData(s) +
                        " Confermare operazione di consuntivazione?",
                        s)
                # Se è un'operazione di primo inserimento
                else:
                    output_statement = Statement_State(
                        "Scelta Fatturabilità accettata : Inserire la descrizione", s)

            elif any(x in text.split() for x in negativo):
                s.addData("fatturabile", "False")
                # Se è un'operazione di modifica
                if dati["conferma"] == "fatturabile":
                    s.addData("conferma", "non confermato")
                    output_statement = Statement_State(
                        "Fatturabilità Accettata e aggiornata. Visualizzazione Dati Aggiornati <br>" +
                        returnAllData(s) +
                        "Confermare operazione di consuntivazione?",
                        s)
                # Se è un'operazione di primo inserimento
                else:
                    output_statement = Statement_State(
                        "Scelta Fatturabilità accettata : Inserire la descrizione", s)
            else:
                output_statement = Statement_State(
                    "Scelta Fatturabilità non accettata : reinserire una risposta corretta ( esempio : sì/no)", s)

        # Utente ha inserito la sede, ora dovrà inserire la descrizione
        elif (not dati["descrizione"] and dati["fatturabile"]) or dati["conferma"] == "descrizione":
            s.addData("descrizione", text)
            # Se è un'operazione di modifica
            if dati["conferma"] == "descrizione":
                s.addData("conferma", "non confermato")
                output_statement = Statement_State(
                    "Descrizione Accettata e aggiornata. Visualizzazione Dati Aggiornati <br>" +
                    returnAllData(s) +
                    " Confermare operazione di consuntivazione?",
                    s)
            # Se è un'operazione di primo inserimento
            else:
                statement = "Descrizione Accettata : Inserimento completato <br>" + \
                    returnAllData(s) + "vuoi consuntivare? ( consuntiva per consuntivare, modifica per modificare, annulla per annullare )"
                output_statement = Statement_State(statement, s)

        # Utente ha inserito tutti i dati richiesti, ora dovrà confermare
        elif dati:
            chiavi = [
                'codice progetto',
                'data',
                'ore fatturabili',
                'ore viaggio',
                'ore viaggio fatturabili',
                'sede',
                'fatturabile',
                'descrizione']

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
                modifica = ['modifica']
                consuntiva = ['sì', 'ok', 'consuntiva', 'procedi', 'conferma']

                if any(x in text.split() for x in consuntiva):
                    s.addData("conferma", "conferma")
                    Req = Request_Activity(s, Api)
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

                elif any(x in text.split() for x in annulla):
                    output_statement = Statement_State(
                        "Operazione annullata", State_Null())

                elif any(x in text.split() for x in modifica):
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
