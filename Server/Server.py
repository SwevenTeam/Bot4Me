from cgi import test
from tkinter.messagebox import NO
from turtle import textinput
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from Server.State.Statement_State import Statement_State
from Server.Adapter.Adapter import Adapter
from Server.State.State_Null import State_Null
from sqlalchemy import null


class Server:
    """
    ---
    Class Name : Server
    ---
    - Description → rappresenta il server che contiene il chatbot
    """

    def __init__(self):
        self.chatterbot = ChatBot("botforme", logic_adapters=[
            {'import_path': 'Server.Adapter.Adapter.Adapter'},
            {'import_path': 'Server.Adapter.Adapter_Login.Adapter_Login'},
            {'import_path': 'Server.Adapter.Adapter_Gate.Adapter_Gate'},
            {'import_path': 'Server.Adapter.Adapter_Undo.Adapter_Undo'},
            {'import_path': 'Server.Adapter.Adapter_Logout.Adapter_Logout'},
            {'import_path': 'Server.Adapter.Adapter_Presence.Adapter_Presence'},
            {'import_path': 'Server.Adapter.Adapter_Activity.Adapter_Activity'},
            {'import_path': 'Server.Adapter.Adapter_Project_Creation.Adapter_Project_Creation'},
            {'import_path': 'Server.Adapter.Adapter_Get_Activity.Adapter_Get_Activity'}])

    def getResponse(self, text, state, apiKey) -> Statement_State:
        """
        ---
        Function Name : getResponse
        ---
        - Args →
          -  text (type String): testo inviato dall'utente
          -  stato (type State): stato del Client al momento dell'invio del messaggio
          -  apiKey (type String): stringa che rappresenza la API Key
        - Description → dato uno Statement_State, controlla tutti gli adapter e restituisce la risposta più adatta
        - Returns → Statement_State value : restituisce la risposta del chatbot con eventuale stato aggiornato
        """
        input_statement = Statement_State(text, state, apiKey)

        max_confidence = -1
        textoutput = ""
        for adapter in self.chatterbot.logic_adapters:
            if adapter.can_process(input_statement):
                output = adapter.process(input_statement, None)

                if output.confidence > max_confidence:
                    textoutput = output
                    max_confidence = output.confidence

        if textoutput == "":
            # Effettuo questa operazione perché vengono effettuate operazioni
            # con i logic adapter per cui servono degli Stati
            if apiKey == null:
                textoutput = Statement_State(
                    "Devi prima effettuare l'accesso per utilizzare i nostri servizi",
                    State_Null(),
                    apiKey)
            else:
                textoutput = Statement_State(
                    "Nessun Logic Adapter Adatto Trovato", State_Null(), apiKey)

        return textoutput
