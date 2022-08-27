import pytest
from ..Adapter import Adapter
from chatterbot import ChatBot
from State.Statement_State import Statement_State
from State.State_Null import State_Null
from ..Util_Adapter import similarStringMatch_Location, getLocationList
from sqlalchemy import null


class Test_Adapter():

    # Creazione Chatbot Temporaneo per Test
    @pytest.fixture
    def chatbot(self):
        return ChatBot("Test")

    # Test Adapter
    #T_U27
    def test_Adapter(self, chatbot):
        S = Statement_State("ciao", State_Null(), null)
        A = Adapter(chatbot)
        if A.can_process(S):
            value = A.process(S, None)
        assert value.text == "Ciao, sono Bot4Me"

    # Test Errore Adapter
    #T_U28
    def test_Adapter_Error(self, chatbot):
        S = Statement_State("non esiste", State_Null())
        A = Adapter(chatbot)
        assert A.can_process(S) == False

    # TEST UTILS
    # Test String Match Location
    def test_Util_Location_Correct(self):
        statement = ['a', 'imola', 'maledetto']
        value = similarStringMatch_Location(
            statement, '12345678-1234-1234-1234-123456789012')
        assert value == 'imola'

    # Test Errore String Match Location
    def test_Util_Location_Error(self):
        value = similarStringMatch_Location("Ciao", '')
        assert value == ''

    # Test Get Location List
    def test_Util_getLocationList_Correct(self):
        value = getLocationList('12345678-1234-1234-1234-123456789012')
        assert value == ['IMOLA', 'BOLOGNA']

    # Test Errore Get Location List
    def test_Util_getLocationList_Error(self):
        value = getLocationList('')
        assert value == []
