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
        textinput = StatementStato(text, stato, apiKey)
        for adapter in self.chatterbot.logic_adapters:
            textoutput = adapter.process(textinput, None)
        return textoutput