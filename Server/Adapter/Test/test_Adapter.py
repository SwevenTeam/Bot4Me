import pytest
from ..Adapter import Adapter
from Client import Client
from Server import Server
from State.State_Presence import State_Presence
from ..Util_Adapter import similarStringMatch_Location, getLocationList


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

    def test_Util_Location_Error(self):
        value = similarStringMatch_Location("Ciao", '')
        assert value == ''

    def test_Util_Location_Correct(self):
        statement = ['a', 'imola', 'maledetto']
        value = similarStringMatch_Location(
            statement, '12345678-1234-1234-1234-123456789012')
        assert value == 'imola'

    def test_Util_getLocationList_Error(self):
        value = getLocationList('')
        assert value == []

    def test_Util_getLocationList_Correct(self):
        value = getLocationList('12345678-1234-1234-1234-123456789012')
        assert value == ['IMOLA', 'BOLOGNA']
