from ..Request_Gate import Request_Gate
from State.State_Gate import State_Gate
from State.State_Null import State_Null


class Test_Request_Gate():

    # T_U48
    def test_Request_Gate_isReady(self):
        S = State_Gate()
        S.addData("sede", "Imola")
        Req = Request_Gate(S, "12345678-1234-1234-1234-123456789012")
        assert Req.isReady()

    # T_U49
    def test_Request_Gate_Error(self):
        S = State_Gate()
        S.addData("sede", "Imola")
        Req = Request_Gate(S, "")
        assert Req.sendRequest() == False
