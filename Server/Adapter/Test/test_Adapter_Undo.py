import pytest
from Client import Client
from Server import Server
from .util import login


def test_ouput_Consuntivazione():
    server = Server()
    client = Client(server)
    login(client)
    client.getResponse("consuntiva")
    value = client.getResponse("annulla")
    assert value == "Operazione di consuntivazione Annullata"


def test_output_Not_Logged():
    server = Server()
    client = Client(server)
    value = client.getResponse("annulla")
    assert value == "Non Sei Loggato e non Hai Operazioni Da Annullare"


def test_output_No_Operation():
    server = Server()
    client = Client(server)
    login(client)
    value = client.getResponse("annulla")
    assert value == "Nessuna Operazione da Annullare"
