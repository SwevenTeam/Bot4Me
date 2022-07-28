from ast import And
from asyncio.windows_events import NULL
from decimal import InvalidOperation
import string
from chatterbot.logic import LogicAdapter
from RequestConsuntivazione import RequestConsuntivazione
from StatementStato import StatementStato
from StatoConsuntivazione import StatoConsuntivazione
from chatterbot.conversation import Statement
from sqlalchemy import false, true

from StatoIniziale import StatoIniziale
class AdapterConsuntivazione(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        # Stato per fare i controlli
        stato=statement.getStato()

        # Se lo Stato è settato a "Iniziale", controllo se l'utente ha inserito consuntivo
        if stato.getStatoAttuale() == "Iniziale":

            #Controllo su presenza stringhe che identificano la richiesta di consuntivazione
            words = ['consuntivazione', 'consuntivare','con', 'consuntiva', 'consuntivo']
            if any(x in statement.text.split() for x in words):
              return True
            else:
              return False

        # Altrimenti, controllo se lo stato è consuntivazione
        elif stato.getStatoAttuale() == "consuntivazione":
            return True

        # Infine, se nessuno dei due if restituiscono vero, questo adapter non potrà effettuare il process
        else:
            return False

    def process(self, input_statement, additional_response_selection_parameters) -> StatementStato:
        
        # s rappresenta lo StatementStato
        s = input_statement.getStato()

        # Nel caso in cui sia settato ad "Iniziale", 
        # riassegno il valore come una nuova inizializzazione di  StatoConsuntivazione
        if s.getStatoAttuale() and s.getStatoAttuale() == "Iniziale":
            s = StatoConsuntivazione()

        # Effettuo dei controlli sul Substate, per sapere cosa dover richiedere all'utente        
        if(s.substate =="inizio"):
            output_statement=StatementStato("Consuntivazione Avviata : Inserire il nome della sede",s)
            s.aggiornamento(input_statement)

        elif(s.substate =="Sede"):
            sedeP = ['Bologna', 'bologna','bl']
            
            sedeI = ['Imola', 'imola', 'im']
             
            if any(x in input_statement.text.split() for x in sedeP):
              output_statement=StatementStato("Sede Accettata : Inserire la descrizione del progetto",s)
              s.aggiornamento(StatementStato("Bologna",s) )
            elif any(x in input_statement.text.split() for x in sedeI):
              output_statement=StatementStato("Sede Accettata : Inserire la descrizione del progetto",s)
              s.aggiornamento(StatementStato("Imola",s))
            else:
              output_statement=StatementStato("Sede non Accettata : Reinserire il nome della Sede",s)

        elif(s.substate =="descrizione"):
            output_statement=StatementStato("Descrizione Accettata : Inserire la data del progetto (formato aaaa-mm-gg)",s)
            s.aggiornamento(input_statement)

        elif(s.substate =="data"):
            ### Da sistemare quando conosco il formato della data
            if True :
              output_statement=StatementStato("Data Accettata : Inserire la durata del progetto",s)
              s.aggiornamento(input_statement)
            else:
              output_statement=StatementStato("Data non Accettata : Reinserire la data del progetto",s)
              
        elif(s.substate =="durata"):
            s.aggiornamento(input_statement)
            values = s.getDati()
            stringa = "Durata Accettata; \n Dati Inseriti : \n"
            for x in values:
              stringa += x +" : "+ values[x] + "\n"
            stringa += " Confermare l'operazione?"
            
            output_statement=StatementStato(stringa,s)
        elif(s.substate =="termina"):
            Req = RequestConsuntivazione(s,input_statement.getApiKey())
            if Req.isReady():
              output_statement=StatementStato(Req.sendRequest(),StatoIniziale())      
            else:
              output_statement=StatementStato("Operazione non avvenuta correttamente, riprovare? (inviare annulla per annullare)",s)      
        else:
            output_statement=StatementStato("È avvenuto un errore sconosciuto",s)

        # Aggiorno il valore di s, il cui stato sarà salvato su Client,
        # in questo modo alla prossima iterazione, il substate sarà 
        # modificato e si procederà con l'inserimento
        
        return output_statement
