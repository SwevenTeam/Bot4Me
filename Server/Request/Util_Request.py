import json
from operator import itemgetter


def IsDictionaryFilled(Dictionary):
    return all(value != '' for value in Dictionary.values())


def parseResponseGetActivity(response):
    outputString = ''
    orderResponse = orderGetActivity(response)
    for i in orderResponse:
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


def orderGetActivity(response):
    return sorted(response, key=itemgetter('date'))
