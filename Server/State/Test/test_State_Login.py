import pytest
from sqlalchemy import null
from ..State_Login import State_Login


class Test_State_Login():

    #T_U17
    def test_State_Login(self):
        SL = State_Login()
        assert SL.getData()['utente'] == ""

    #T_U18
    def test_State_Login_Data(self):
        SL = State_Login()
        SL.addData("utente", "Pippo")
        assert SL.getData()['utente'] == "Pippo"

    #T_U19
    def test_State_Login_Error(self):
        SL = State_Login()
        SL.addData("utentino", "Pippo")
        assert SL.getData()['utente'] == ""
