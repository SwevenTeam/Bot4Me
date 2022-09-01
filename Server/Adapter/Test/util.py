
def ModifyActivity(Sa):
    Sa.addData('codice progetto', "1")
    Sa.addData('data', "2022-01-01")
    Sa.addData('ore fatturabili', "3")
    Sa.addData('ore viaggio', "3")
    Sa.addData('ore viaggio fatturabili', "3")
    Sa.addData('sede', "imola")
    Sa.addData('fatturabile', "True")
    Sa.addData('descrizione', "descrizione esempio")
    return Sa


def ModifyCreation(Sc):
    Sc.addData('codice progetto', "1999")
    Sc.addData('dettagli', "template description")
    Sc.addData('cliente', "template client")
    Sc.addData('manager', "template manager")
    Sc.addData('status', "iniziale")
    Sc.addData('area', "Bologna")
    Sc.addData('data Inizio', "2022-01-01")
    Sc.addData('data Fine', "2022-01-02")
    return Sc
