
def getAllergyInfo(req):
    result = req.get('result')

    parameters = result.get('parameters')

    allergens = parameters.get('allergen')

    data = {}
    data['sessionId'] = req.get('sessionId')

    if allergens:
        data['allergens'] = allergens

    return data
    
def setAllergiesIntent(req):
    data = getAllergyInfo(req)
    
    if data is None:
        return {}

    # TODO : save allergies related to sessionId somewhere

    speech = 'So you\'re allergic to: '
    for allergen in data['allergens']:
        speech += allergen + ', '
    speech = speech[:-2]

    json_response = {  
       "speech": speech,
       "displayText": speech,
       "source":"jarvis-on-apiai"
    }

    if json_response is None:
        print("problem")

    return json_response

def getAllergiesIntent(req):
    data = {}
    data['sessionId'] = req['sessionId']
    
    if data is None:
        return {}

    # TODO : get allergies related to sessionId
    speech = 'You\'re allergic to: tomato, garlic and pasta. Sorry mate.'

    json_response = {  
       "speech": speech,
       "displayText": speech,
       "source":"jarvis-on-apiai"
    }

    if json_response is None:
        print("problem")

    return json_response

