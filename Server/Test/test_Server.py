from re import S
from Adapter import Adapter
from Server import Server
from Client import Client
from State.State import State
import pytest
from sqlalchemy import null


class Test_Server():

    @pytest.fixture
    def server(self):
        return Server()

    def test_Server_No_Login(self, server):
        client = Client(server)
        value = client.getResponse("esempio")
        assert value == "Devi prima effettuare l'accesso per utilizzare i nostri servizi"

    def test_Server_No_Adapter(self, server):
        client = Client(server)
        client.getResponse("login")
        client.getResponse("12345678-1234-1234-1234-123456789012")
        value = client.getResponse("esempio")
        assert value == "Nessun Logic Adapter Adatto Trovato"

    def test_Double_Adapter(self, server):
        client = Client(server)
        client.getResponse("login")
        client.getResponse("12345678-1234-1234-1234-123456789012")
        value = client.getResponse("annulla get con")
        assert value == "Nessuna Operazione da Annullare"

    def test_Adapter_Update(self, server):
        client = Client(server)
        client.getResponse("login")
        client.getResponse("12345678-1234-1234-1234-123456789012")
        client.getResponse("presenza")
        value = (client.state.getCurrentState() == "presenza Sede")
        client.getResponse("Imola")
        assert client.state.getCurrentState() == "Iniziale" and value
