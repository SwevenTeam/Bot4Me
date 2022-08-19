import pytest
from State.Statement_State import Statement_State
from State.State_Null import State_Null
from chatterbot import ChatBot
from Adapter.Adapter_Gate import Adapter_Gate
from State.State_Gate import State_Gate


class Test_Adapter_Gate():

    # Creazione Chatbot Temporaneo per Test
    @pytest.fixture
    def chatbot(self):
        return ChatBot("Test")

    # Test Avvio Apertura Cancello
    def test_Adapter_Gate_Activate(self, chatbot):
        S = Statement_State("apertura cancello", State_Null())
        A = Adapter_Gate(chatbot)
        if A.can_process(S):
            value = A.process(S, None)
        assert value.text == "Apertura cancello avviata : Inserire la sede del cancello"

    '''
    def test_Adapter_Gate_Location_Correct(self,chatbot):
        client = Client(server)
        login(client)
        client.getResponse("cancello")
        value = client.getResponse("IMOLA")
        assert value == "Sede accettata : Richiesta apertura del cancello avvenuta con successo"
    '''
    # Test Apertura Cancello Sede Incorretta

    def test_Adapter_Presence_Location_Incorrect(self, chatbot):
        S = Statement_State(
            "Imolaaaaaa",
            State_Gate(),
            '12345678-1234-1234-1234-123456789012')
        A = Adapter_Gate(chatbot)
        if A.can_process(S):
            value = A.process(S, None)
        assert value.text == "Sede non trovata : Reinserire la sede del cancello"
