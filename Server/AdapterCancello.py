from Adapter import Adapter
from RequestCancello import RequestCancello
from StatementStato import StatementStato
from StatoCancello import StatoCancello
from StatoIniziale import StatoIniziale


class AdapterCancello(Adapter):
    """
    ---
    Class Name : AdapterCancello 
    ---
    - Args → Adapter ( type Adapter) : implementata da tutti gli adapter di Chatbot
    - Description → Adapter per l'apertura del cancello di una sede
    """

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement: StatementStato):
        """
        ---
        Function Name : can_process
        ---
        - Args → statement ( type StatementStato) : frase input presa dal client
        - Description → restituisce True se l'elemento in Input contiene keyword corretta o stato uguale a cancello
        - Returns → boolean value : true se può eseguire, false se non può eseguire
        """
        stato = statement.getStato()

        if stato.getStatoAttuale() == StatoCancello().getStatoAttuale():
            return True

        if stato.getStatoAttuale() == StatoIniziale().getStatoAttuale():
            words = ['cancello', 'varco', 'entrata', 'apertura', 'apri']
            return any(word in statement.text.split() for word in words)

        return False

    def process(self, input_statement: StatementStato, additional_response_selection_parameters) -> StatementStato:
        """
        ---
        Function Name :  process
        ---
        - Args → 
          - input_statement ( type StatementStato): frase inserita dall'utente
          - additional_response_selection_parameters ( type any): elementi extra necessari alla funzione del metodo
        - Description → 
        crea un outputStatement (StatementStato) in base all'input inserito dall'utente, nel caso inserisca una sede valida 
        richiede l'apertura del cancello
        - Returns → StatementStato value : risposta del chatbot con eventuale cambio di stato
        """
        stato = input_statement.getStato()

        # L'Utente vuole avviare l'attività di apertura del cancello
        if stato.getStatoAttuale() == StatoIniziale().getStatoAttuale():
            return StatementStato(
                "Apertura cancello avviata : Inserire la sede del cancello",
                StatoCancello(),
                input_statement.getApiKey()
            )

        
        request_cancello = RequestCancello(input_statement.getApiKey())
        # vengono recuperate le sedi
        locations = request_cancello.getLocations()

        if len(locations) > 0:
            # validazione della sede
            sede = ''
            for word in input_statement.getText().split():
                if word.upper() in locations:
                    sede = word.upper()
                    break

            if sede == '':
                return StatementStato(
                    "Sede non trovata : Reinserire la sede del cancello",
                    stato,
                    input_statement.getApiKey()
                )

            stato.addDati("sede", sede)
            request_cancello.setSede(stato)

            # viene inviata la richiesta di apertura del cancello, se non va a buon fine si è verificato un errore
            if request_cancello.isReady() and request_cancello.sendRequest():
                return StatementStato(
                    "Sede accettata : Richiesta apertura del cancello avvenuta con successo",
                    StatoIniziale(),
                    input_statement.getApiKey()
                )

        return StatementStato(
            "Si è verificato un errore sconosciuto, riprova ad inviare la sede",
            stato,
            input_statement.getApiKey()
        )
