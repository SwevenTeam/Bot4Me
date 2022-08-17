import pytest
from sqlalchemy import null
from ..State_Login import State_Login

class Test_State_Login():

    def test_State_Login_Data_Null(self):
        SL = State_Login()
        assert SL.getData()['utente'] == ""

    def test_State_Login_Data(self):
        SL = State_Login()
        SL.addData("utente","Pippo")
        assert SL.getData()['utente'] == "Pippo"

    def test_State_Login_Error(self):
        SL = State_Login()
        SL.addData("utentino","Pippo")
        assert SL.getData()['utente'] == ""