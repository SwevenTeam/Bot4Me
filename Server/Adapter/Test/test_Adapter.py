import pytest
from Client import Client
from Server import Server


def test_Adapter():
    server = Server()
    client = Client(server)
    value = client.getResponse("ciao")
    assert value == "Ciao, sono Bot4Me"
