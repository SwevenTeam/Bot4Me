from cgi import test
from tkinter.messagebox import NO
from turtle import textinput
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from StatementStato import StatementStato
from Adapter import Adapter

class Server:
    def __init__(self):
        self.chatterbot = ChatBot("botforme",logic_adapters=[{'import_path': 'Adapter.Adapter'}])
    
    def getResponse(self, text, stato, apiKey) -> StatementStato:
        input_statement=StatementStato(text,stato,apiKey)
        max_confidence = -1
        for adapter in self.chatterbot.logic_adapters:
            if adapter.can_process(input_statement):
                output = adapter.process(input_statement, None)

                if output.confidence > max_confidence:
                    textoutput = output
                    max_confidence = output.confidence
        return textoutput