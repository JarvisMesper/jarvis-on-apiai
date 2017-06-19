from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json

def get_forecast(req):
    print ("Asking weather forecast to Yahoo")
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = makeYqlQuery(req)
    if yql_query is None:
        print ("Problem, can't creat YQL Query")
        return {}
    print ("YQL Query:")
    print (yql_query)
    yql_url = baseurl + urlencode({'q': yql_query}) + "&format=json"
    print ("YQL Url:")
    print (yql_url)
    result = urlopen(yql_url).read().decode("utf8")
    print ("Result:")
    print(result)
    data = json.loads(result)

    return data

def makeYqlQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    if city is None:
        return None

    return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"


def makeForecastWebhookResult(req):
    data = get_forecast(req)
    if data is None:
        return {}

    query = data.get('query')
    if query is None:
        return {}

    result = query.get('results')
    if result is None:
        return {}

    channel = result.get('channel')
    if channel is None:
        return {}

    linktemp = channel.get('link')
    link = None
    if linktemp is not None:
        linktemp = linktemp.split("*")
        if len(linktemp) > 1:
            link = linktemp[1]

    item = channel.get('item')
    location = channel.get('location')
    units = channel.get('units')
    if (location is None) or (item is None) or (units is None):
        return {}

    condition = item.get('condition')
    if condition is None:
        return {}

    # print(json.dumps(item, indent=4))
    tempF = int(condition.get('temp'))
    print ("Temperature in Farenheit: ")
    print (tempF)

    tempC = int((tempF - 32) * (5.0 / 9.0) + 0.5)
    print ("Temp in Celsius: ")
    print (tempC)

    speech = "Today in " + location.get('city') + ": " + condition.get('text') + \
             ", the temperature is " + str(tempC) + " " + "°C"

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        "data": {"facebook": {
                    "attachment": {
                        "type": "template",
                        "payload":{
                            "template_type":"button",
                            "text":speech,
                            "buttons":[
                            {
                                "type":"web_url",
                                "url":link,
                                "title":"See on Yahoo Weather forecast"
                            }
                            ]
                        }
                    }
                 }
        },
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample",
    }