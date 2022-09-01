import pytest
from sqlalchemy import null
from ..State_Activity import State_Activity


class Test_State_Activity:

    # T_U10
    def test_State_Activity(self):
        SG = State_Activity()
        assert SG.getData()['sede'] == ""

    # T_U11
    def test_State_Activity_Correct(self):
        SG = State_Activity()
        SG.addData("sede", "Imola")
        assert SG.getData()['sede'] == "Imola"

    # T_U12
    def test_State_Activity_Incorrect(self):
        SG = State_Activity()
        SG.addData("sedee", "Imola")
        assert SG.getData()['sede'] == ""
