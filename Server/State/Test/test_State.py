import pytest
from sqlalchemy import null
from ..State import State

#T_U9
def test_State():
    S = State()
    assert S.getData() is None
    assert S.getCurrentState() is None
