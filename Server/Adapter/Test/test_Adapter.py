import pytest
from ..Adapter import Adapter
from Client import Client
from Server import Server


class Test_Adapter():

    @pytest.fixture
    def server(self):
        return Server()

    def test_Adapter(self, server):
        client = Client(server)
        value = client.getResponse("ciao")
        assert value == "Ciao, sono Bot4Me"

    def test_Adapter_Error(self, server):
        client = Client(server)
        value = client.getResponse("non esiste")
        assert value == "Devi prima effettuare l'accesso per utilizzare i nostri servizi"
