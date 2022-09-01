import pytest
from sqlalchemy import null
from ..State_Get_Activity import State_Get_Activity


class Test_State_Get_Activity:

    # T_U16
    def test_State_Get_Activity(self):
        SG = State_Get_Activity()
        assert SG.getData()['codice progetto'] == ""
