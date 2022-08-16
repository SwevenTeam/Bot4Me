import pytest
from ..Adapter import Adapter
from Client import Client
from Server import Server
from .util import login


class Test_Adapter_Undo():

    @pytest.fixture
    def server(self):
        return Server()

    def test_ouput_Consuntivazione(self, server):
        client = Client(server)
        login(client)
        client.getResponse("consuntiva")
        value = client.getResponse("annulla")
        assert value == "Operazione di consuntivazione Annullata"

    def test_output_Not_Logged(self, server):
        client = Client(server)
        value = client.getResponse("annulla")
        assert value == "Non Sei Loggato e non Hai Operazioni Da Annullare"

    def test_output_No_Operation(self, server):
        client = Client(server)
        login(client)
        value = client.getResponse("annulla")
        assert value == "Nessuna Operazione da Annullare"
