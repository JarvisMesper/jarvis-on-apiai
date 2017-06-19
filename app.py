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
from actions import place

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)
    res = json.dumps(res, indent=4)

    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


@app.route('/webhook', methods=['GET'])
def webhook_challenge():
    """
    A webhook to return a challenge
    """
    verify_token = request.args.get('hub.verify_token')
    print(verify_token)
    print("Verified token")

    # check whether the verify tokens match
    if verify_token == "api_token":
        # respond with the challenge to confirm
        challenge = request.args.get('hub.challenge')
        return challenge
    else:
        return 'Invalid Request or Verification Token'


def processRequest(req):
    print("processing Request")
    res = None
    if req.get("result").get("action") == "weatherForecast":
        print("process weather request")
        res = forecast.makeForecastWebhookResult(req)
    if req.get("result").get("action") == "productInfo":
        print("process openfood request")
        res = openfood.makeProductInfoWebhookResult(req)
    if req.get("result").get("action") == "storeLocation":
        print("process place request")
        res = place.makeStoreLocationWebhookResult(req)

    print('========== RES ==========')
    print(res)
    return res


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
