import pytest
from State.Statement_State import Statement_State
from State.State_Null import State_Null
from State.State_Presence import State_Presence
from chatterbot import ChatBot
from Adapter.Adapter_Presence import Adapter_Presence
from sqlalchemy import null


class Test_Adapter():

    # Creazione Chatbot Temporaneo per Test
    @pytest.fixture
    def chatbot(self):
        return ChatBot("Test")

    # Test Avvio Registrazione Presenza
    def test_Adapter_Presence_Activate(self, chatbot):
        S = Statement_State(
            "presenza",
            State_Null(),
            '12345678-1234-1234-1234-123456789012')
        A = Adapter_Presence(chatbot)
        if A.can_process(S):
            value = A.process(S, None)
        assert value.text == "Operazione di registrazione della presenza avviata : inserire il nome di una sede"

    # Test Registrazione Presenza Corretta
    @pytest.mark.parametrize("sede", [("Imola"), ("Bologna")])
    def test_Adapter_Presence_Location_Correct(self, sede, chatbot):
        S = Statement_State(
            sede,
            State_Presence(),
            '12345678-1234-1234-1234-123456789012')
        A = Adapter_Presence(chatbot)
        if A.can_process(S):
            value = A.process(S, None)
        assert value.text == "Registrazione presenza effettuata con Successo"

    '''
    # Test Registrazione Presenza Incorretta - Api
    def test_Adapter_Presence_Location_Api_Error(self, chatbot):
        S = Statement_State("Imola",State_Presence(),'12345678-1234-1234-1234-123456789012')
        A = Adapter_Presence(chatbot)
        if A.can_process(S):
            value = A.process(S,None)
        else:
            value = null
        assert value.text == "Registrazione presenza Fallita"
    '''
    # Test Registrazione Presenza Incorretta

    def test_Adapter_Presence_Location_Incorrect(self, chatbot):
        S = Statement_State(
            "Padova",
            State_Presence(),
            '12345678-1234-1234-1234-123456789012')
        A = Adapter_Presence(chatbot)
        if A.can_process(S):
            value = A.process(S, None)
        assert value.text == "Sede non Accettata : Reinserire il nome della Sede"
