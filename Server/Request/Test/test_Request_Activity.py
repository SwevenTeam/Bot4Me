from ..Request_Activity import Request_Activity
from State.State_Activity import State_Activity
from State.State_Null import State_Null


class Test_Request_Activity():

    # T_U46
    def test_Request_Activity_isReady(self):
        S = State_Activity()
        S.addData("codice progetto", "1")
        S.addData("data", "2022-05-01")
        S.addData("ore fatturabili", "5")
        S.addData("ore viaggio", "5")
        S.addData("ore viaggio fatturabili", "5")
        S.addData("sede", "Imola")
        S.addData("fatturabile", "True")
        S.addData("descrizione", "descrizione")
        S.addData("conferma", "conferma")
        Req = Request_Activity(S, "12345678-1234-1234-1234-123456789012")
        assert Req.isReady()

    def test_Request_Activity_isReady_Error_Type(self):
        S = State_Null()
        Req = Request_Activity(S, "12345678-1234-1234-1234-123456789012")
        assert Req.isReady() == False

    # U_T47
    def test_Request_Activity_isReady_Error_Not_Ready(self):
        S = State_Activity()
        Req = Request_Activity(S, "12345678-1234-1234-1234-123456789012")
        assert Req.isReady() == False

    def test_Request_Activity_SendRequest_Error_Not_Ready(self):
        S = State_Activity()
        Req = Request_Activity(S, "")
        assert Req.sendRequest() == False
