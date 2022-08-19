import pytest
from State.Statement_State import Statement_State
from State.State_Null import State_Null
from State.State_Login import State_Login
from chatterbot import ChatBot
from Adapter.Adapter_Login import Adapter_Login
from sqlalchemy import null


class Test_Adapter_Login():

    # Creazione Chatbot Temporaneo per Test
    @pytest.fixture
    def chatbot(self):
        return ChatBot("Test")


    def test_Adapter_Login_Activate(self, chatbot):
        S = Statement_State("login",State_Null(),null)
        A = Adapter_Login(chatbot)
        if A.can_process(S):
            value = A.process(S,None)
        assert value.text == "Autenticazione Avviata : Inserire l'API-KEY"


    def test_Adapter_Login_Api_Correct(self, chatbot):
        S = Statement_State("12345678-1234-1234-1234-123456789012",State_Login(),null)
        A = Adapter_Login(chatbot)
        if A.can_process(S):
            value = A.process(S,None)
        assert value.text == "Autenticazione Avvenuta Con Successo"


    def test_Adapter_Login_Api_Incorrect(self, chatbot):
        S = Statement_State("1",State_Login(),null)
        A = Adapter_Login(chatbot)
        if A.can_process(S):
            value = A.process(S,None)
        assert value.text == "Autenticazione Fallita : l'API-KEY inserita non è valida, riprova"

    def test_Adapter_Login_Already_Logged(self, chatbot):
        S = Statement_State("login",State_Null(),"12345678-1234-1234-1234-123456789012")
        A = Adapter_Login(chatbot)
        if A.can_process(S):
            value = A.process(S,None)
        assert value.text == "Hai già effettuato l'accesso"
