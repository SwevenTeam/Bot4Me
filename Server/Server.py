from cgi import test
from tkinter.messagebox import NO
from turtle import textinput
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from StatementStato import StatementStato
from Adapter import Adapter
from StatoIniziale import StatoIniziale

class Server:
    def __init__(self):
        self.chatterbot = ChatBot("botforme",logic_adapters=[{'import_path': 'Adapter.Adapter'},{'import_path': 'AdapterPresenza.AdapterPresenza'},{'import_path': 'AdapterAnnulla.AdapterAnnulla'},{'import_path': 'AdapterConsuntivazione.AdapterConsuntivazione'}])
    
    def getResponse(self, text, stato, apiKey) -> StatementStato:
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
            textoutput = StatementStato("Nessun Logic Adapter Adatto Trovato",StatoIniziale(),apiKey)
        return textoutput