

def IsDictionaryFilled(Dictionary):
    return all(value != '' for value in Dictionary.values())


def parseResponse(response):
    str = response.replace("[", "")
    str.replace("]", "")
    str.replace(",", "<br>")
    str.replace("}", "<br>")
    return str.replace("{", "CONSUNTIVAZIONE")
