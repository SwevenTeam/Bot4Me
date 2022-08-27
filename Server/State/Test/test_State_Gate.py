import pytest
from sqlalchemy import null
from ..State_Gate import State_Gate


class Test_State_Gate:

    #T_U13
    def test_State_Gate(self):
        SG = State_Gate()
        assert SG.getData()['sede'] == ""

    #T_U14
    def test_State_Gate_Correct(self):
        SG = State_Gate()
        SG.addData("sede", "Imola")
        assert SG.getData()['sede'] == "Imola"

    #T_U15
    def test_State_Gate_Incorrect(self):
        SG = State_Gate()
        SG.addData("sedee", "Imola")
        assert SG.getData()['sede'] == ""
