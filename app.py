from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response


from actions import openfood
from actions import forecast

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    data = None
    if req.get("result").get("action") == "weatherForecast":
        data = forecast.get_forecast(req)
    if req.get("result").get("action") == "openfoodInfo":
        #res = makeWebhookResult(data)
        print("nothing yet")

    print("Data:")
    print(data)
    res = makeWebhookResult(data)
    print("Res:")
    print(res)
    return res



def makeWebhookResult(data):
    query = data.get('query')
    if query is None:
        return {}

    result = query.get('results')
    if result is None:
        return {}

    channel = result.get('channel')
    if channel is None:
        return {}

    item = channel.get('item')
    location = channel.get('location')
    units = channel.get('units')
    if (location is None) or (item is None) or (units is None):
        return {}

    condition = item.get('condition')
    if condition is None:
        return {}

    # print(json.dumps(item, indent=4))

    speech = "Today in " + location.get('city') + ": " + condition.get('text') + \
             ", the temperature is " + condition.get('temp') + " " + units.get('temperature')

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
                            "url":"https://petersapparel.parseapp.com",
                            "title":"See on Yahoo Weather forecast"
                          },
                          {
                            "type":"postback",
                            "title":"Go fuck yourself",
                            "payload":"USER_DEFINED_PAYLOAD"
                          }
                        ]
                      }
                    }
                 }
        },
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample",
        
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print(forecast.testPrint("bitch"))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
