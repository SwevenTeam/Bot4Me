import pytest
from Adapter.Adapter_Undo import Adapter_Undo
from chatterbot import ChatBot
from State.Statement_State import Statement_State
from State.State_Null import State_Null
from State.State_Presence import State_Presence
from sqlalchemy import null


class Test_Adapter_Undo():

    # Creazione Chatbot Temporaneo per Test
    @pytest.fixture
    def chatbot(self):
        return ChatBot("Test")

    # Test Adapter Undo /w Presence
    #T_U44
    def test_Adapter_Undo_Presence(self, chatbot):
        S = Statement_State("annulla", State_Presence())
        A = Adapter_Undo(chatbot)
        if A.can_process(S):
            value = A.process(S, None)
        assert value.text == "Operazione di presenza Sede Annullata"

    # Test Adapter Undo - Nothing to Undo and Unlogged
    def test_output_Not_Logged(self, chatbot):
        S = Statement_State("annulla", State_Null(), null)
        A = Adapter_Undo(chatbot)
        value = A.process(S, None)
        assert value.text == "Non Sei Loggato e non Hai Operazioni Da Annullare"

    # Test Adapter Undo - Nothing to Undo and Logged
    #T_U45
    def test_output_No_Operation(self, chatbot):
        S = Statement_State("annulla", State_Null(), '123')
        A = Adapter_Undo(chatbot)
        value = A.process(S, None)
        assert value.text == "Nessuna Operazione da Annullare"
