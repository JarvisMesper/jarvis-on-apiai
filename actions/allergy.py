from utils import utils
from actions.DBClient import DBClient

saveToMongo = True  # If False, it's saved to a file

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

    if saveToMongo:
        # save allergies to mongodb
        db = DBClient.get_db()
        session = db.sessions.find_one({'sessionId': data['sessionId']})

        if session and 'allergies' in session:
            # this user already has allergies
            my_allergies = session['allergies']
        else:
            # no previous allergies
            my_allergies = []

        for allergen in data['allergens']:
            if allergen not in my_allergies:
                my_allergies.append(allergen)

        if session and 'sessionId' in session:
            # update user data
            db.sessions.update({'sessionId': data['sessionId']},{'$set': {'allergies': my_allergies}})
        else:
            # new entry in db
            new_session = { 'sessionId': data['sessionId'], 'allergies': my_allergies }
            db.sessions.insert(new_session)
    else:
        # save allergies to a file
        allergies = utils.open_json_file('data/', 'allergies.json')
        if data['sessionId'] in allergies['data']:
            my_allergies = allergies['data'][data['sessionId']]
        for allergen in data['allergens']:
            if allergen not in my_allergies:
                my_allergies.append(allergen)
        allergies['data'][data['sessionId']] = my_allergies
        utils.save_json_file('data/', 'allergies.json', allergies)

    # generate answer
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

    if saveToMongo:
        db = DBClient.get_db()
        session = db.sessions.find_one({'sessionId': data['sessionId']}, {'_id':0,'allergies':1})

        if session and 'allergies' in session:
            speech = 'From what I know, you\'re allergic to: '
            for allergen in session['allergies']:
                speech += allergen + ', '
            speech = speech[:-2]
        else:
            speech = 'I am not aware that you are allergic to anything.'
    else:
        allergies = utils.open_json_file('data/', 'allergies.json')
        if data['sessionId'] in allergies['data']:
            speech = 'From what I know, you\'re allergic to: '
            for allergen in allergies['data'][data['sessionId']]:
                speech += allergen + ', '
            speech = speech[:-2]

        else:
            speech = 'I am not aware that you are allergic to anything.'

    json_response = {  
       "speech": speech,
       "displayText": speech,
       "source":"jarvis-on-apiai"
    }

    if json_response is None:
        print("problem")

    return json_response
