import requests
import os

def getStoreInfo(req):
    result = req.get('result')
    parameters = result.get('parameters')

    store = parameters.get('storeName')
    city = parameters.get('geo-city')

    data = {}

    if store and city:
        data['store'] = store
        data['city'] = city

    return data
    
def makeStoreLocationWebhookResult(req):
    data = getStoreInfo(req)
    
    if data is None:
        return {}

    lat,lng = get_coordinates(data['city'])
    stores_quantity = get_store(data['store'], lat, lng)

    image_url = 'http://icons.iconarchive.com/icons/paomedia/small-n-flat/1024/shop-icon.png'

    speech = 'There are ' + str(stores_quantity) + ' ' + data['store'] + ' in the city of ' + data['city'] + '!'

    json_response = {  
       "speech":speech,
       "displayText":speech,
       "data":{  
          "facebook":{  
             "attachment":{  
                "type":"template",
                "payload":{  
                   "template_type":"generic",
                   "elements":[  
                      {  
                         "title":speech,
                         "image_url":image_url
                      }
                   ]
                }
             }
          }
       },
       "source":"jarvis-on-apiai"
    }

    if json_response is None:
        print("problem")

    return json_response

def get_coordinates(city):
    req = 'https://maps.googleapis.com/maps/api/geocode/json?'
    req += 'address=' + city
    req += '&key=' + os.environ.get('GOOGLE_MAPS_GEOCODING_API_KEY')

    print('---------- get coordinates for ' + city + ' ----------')

    r = requests.get(req)

    resp = r.json()
    lat = resp['results'][0]['geometry']['location']['lat']
    lng = resp['results'][0]['geometry']['location']['lng']

    print('------ ==> lat: ' + str(lat) + ', lng:' + str(lng) + ' ----------')
    return lat, lng

def get_store(store, lat, lng):
    req = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
    req += 'location=' + str(lat) + ',' + str(lng)
    req += '&radius=' + '5000'
    req += '&type=restaurant'
    req += '&keyword=' + store
    req += '&key=' + os.environ.get('GOOGLE_PLACES_API_KEY')

    print('---------- get stores ----------')

    r = requests.get(req)

    resp = r.json()
    count = len(resp['results'])

    # example of response:
    #{
    #    'html_attributions': [], 
    #    'results': [
    #        {
    #            'reference': 'CmRRAAAAQdHuOkIlW3nbWcioPHXS6ZYow', 
    #            'scope': 'GOOGLE', 
    #            'name': 'Migros Restaurant', 
    #            'geometry': {
    #                'location': {'lng': 7.1523113, 'lat': 46.79978680000001}, 
    #                'viewport': {
    #                    'southwest': {'lng': 7.151085519708498, 'lat': 46.7984617697085}, 
    #                    'northeast': {'lng': 7.153783480291502, 'lat': 46.8011597302915}
    #                }
    #            }, 
    #            'id': '7ff650cfe7e675f3792a9caf55ae8f834486337e', 
    #            'vicinity': 'Boulevard de Pérolles 21 A, Fribourg', 
    #            'place_id': 'ChIJ18tK2StpjkcRVVbxV4ZQ7Do', 
    #            'types': ['restaurant', 'cafe', 'food', 'point_of_interest', 'establishment'], 
    #            'opening_hours': {'weekday_text': [], 'open_now': True}, 
    #            'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/restaurant-71.png'
    #        }
    #    ], 
    #    'status': 'OK'
    #}
    
    print('------ ==> stores quantity: ' + str(count) + ' ----------')
    return count