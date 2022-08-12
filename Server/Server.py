from cgi import test
from tkinter.messagebox import NO
from turtle import textinput
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from StatoLogin import StatoLogin
from StatementStato import StatementStato
from Adapter import Adapter
from StatoIniziale import StatoIniziale
from sqlalchemy import null



class Server:
    """
    ---
    Class Name : Server
    ---    
    - Description → rappresenta il server che contiene il chatbot
    """    
    def __init__(self):
        self.chatterbot = ChatBot("botforme",logic_adapters=[
            {'import_path': 'Adapter.Adapter'},
            {'import_path': 'AdapterLogin.AdapterLogin'},
            {'import_path': 'AdapterAnnulla.AdapterAnnulla'},
            {'import_path': 'AdapterLogout.AdapterLogout'},
            {'import_path': 'AdapterPresenza.AdapterPresenza'},
            {'import_path': 'AdapterAnnulla.AdapterAnnulla'},
            {'import_path': 'AdapterConsuntivazione.AdapterConsuntivazione'},
            {'import_path': 'AdapterCreazioneProgetto.AdapterCreazioneProgetto'}])
    
    def getResponse(self, text, stato, apiKey) -> StatementStato:
        """
        ---
        Function Name : getResponse 
        ---
        - Args →
          -  text (type String): testo inviato dall'utente
          -  stato (type Stato): stato del Client al momento dell'invio del messaggio
          -  apiKey (type String): stringa che rappresenza la API Key
        - Description → dato uno StatementStato, controlla tutti gli adapter e restituisce la risposta più adatta
        - Returns → StatementStato value : restituisce la risposta del chatbot con eventuale stato aggiornato
        """      
        input_statement=StatementStato(text,stato,apiKey)

        max_confidence = -1
        textoutput = ""
        for adapter in self.chatterbot.logic_adapters:
            if adapter.can_process(input_statement):
                output = adapter.process(input_statement, None)

                if output.confidence > max_confidence:
                    textoutput = output
                    max_confidence = output.confidence

        if textoutput == "":
            # Effettuo questa operazione perché vengono effettuate operazioni con i logic adapter per cui servono degli Stati
            if apiKey == null:    
              textoutput = StatementStato("Devi prima effettuare l'accesso per utilizzare i nostri servizi",StatoIniziale(),apiKey)
            else:
                textoutput = StatementStato("Nessun Logic Adapter Adatto Trovato",StatoIniziale(),apiKey)
            
        return textoutput