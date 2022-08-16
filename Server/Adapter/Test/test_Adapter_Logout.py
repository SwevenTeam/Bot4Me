import pytest
from ..Adapter import Adapter
from Client import Client
from Server import Server
from .util import login


class Test_Adapter_Logout():

    @pytest.fixture
    def server(self):
        return Server()

    def test_Logout_Correct(self, server):
        client = Client(server)
        login(client)
        value = client.getResponse("logout")
        assert value == "Logout avvenuto con successo"

    def test_Logout_Incorrect(self, server):
        client = Client(server)
        value = client.getResponse("logout")
        assert value == "Devi prima effettuare l'accesso per utilizzare i nostri servizi"
