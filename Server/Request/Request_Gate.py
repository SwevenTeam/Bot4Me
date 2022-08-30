import requests
from Request.MyRequest import MyRequest


class Request_Gate(MyRequest):

    def __init__(self, s, api_key):
        self.state = s.getCurrentState()
        self.data = s.getData()
        self.Api = api_key

    def isReady(self) -> bool:
        """
        ---
        Function Name : isReady
        ---
        - Args → None
        - Description → identifica se questa Request può essere utilizzata
        - Returns → boolean value : true se può eseguire, false se non può eseguire
        """
        if self.state == "cancello":
            if self.data["sede"] == "":
                return False
            else:
                return True
        else:
            return False

    def sendRequest(self) -> bool:
        """
        ---
        Function Name : sendRequest
        ---
        - Args → None
        - Description → assembla la richiesta di apertura del cancello e la invia
        - Returns → boolean value : true se ha eseguito, false altrimenti
        """
        # da cambiare URL con quello reale
        # https://apibot4me.imolinfo.it/v1/locations/imola/devices/example/status
        url = 'https://apibot4me.imolinfo.it/v1/locations/' + \
            self.data['sede'] + '/devices/cancello/status'
        header = {
            'accept': 'application/json',
            'api_key': self.Api,
            'Content-Type': 'application/json'}
        data = {'status': 'string', }

        responseUrl = requests.put(url, headers=header, json=data)
        print(responseUrl)
        if responseUrl.status_code >= 200 and responseUrl.status_code < 300:
            return True
        return False
