import pytest
from State.Statement_State import Statement_State
from State.State_Null import State_Null
from chatterbot import ChatBot
from Adapter.Adapter_Logout import Adapter_Logout
from sqlalchemy import null


class Test_Adapter_Logout():

    # Creazione Chatbot Temporaneo per Test
    @pytest.fixture
    def chatbot(self):
        return ChatBot("Test")

    # Test Logout
    #T_U37
    def test_Logout_Correct(self, chatbot):
        S = Statement_State(
            "logout",
            State_Null(),
            '12345678-1234-1234-1234-123456789012')
        A = Adapter_Logout(chatbot)
        if A.can_process(S):
            value = A.process(S, None)
        assert value.text == "Logout avvenuto con successo"

    # Test Errore Logout
    #T_U38
    def test_Logout_Incorrect(self, chatbot):
        S = Statement_State("logout", State_Null(), null)
        A = Adapter_Logout(chatbot)
        assert A.can_process(S) == False
