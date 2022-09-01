import pytest
from sqlalchemy import null
from ..State_Null import State_Null

# T_U20


def test_State_Null():
    SN = State_Null()
    assert SN.getData() == null
