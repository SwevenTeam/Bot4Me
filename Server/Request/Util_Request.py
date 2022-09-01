import json


def IsDictionaryFilled(Dictionary):
    return all(value != '' for value in Dictionary.values())


def parseResponseGetActivity(response):
    outputString = ''
    for i in response:
        tmp_str = "Consuntivazione del giorno "
        tmp_str += i['date']
        tmp_str += " in sede "
        tmp_str += i['location']
        tmp_str += '<br>'
        tmp_str += "Ore Fatturabili : " + str(i['billableHours']) + "<br>"
        tmp_str += "Ore di viaggio : " + str(i['travelHours']) + "<br>"
        tmp_str += "Ore di viaggio Fatturabili : " + \
            str(i['billableTravelHours']) + "<br>"
        tmp_str += "descrizione : " + i['note'] + "<br><br>"
        outputString += tmp_str
    return outputString
