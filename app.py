import json
import os

from actions import allergy
from actions import forecast
from actions import openfood
from actions import place

from flask import Flask
from flask import make_response
from flask import request


# Flask app should start in global layout
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    content = '<h1>Jarv webhook</h1>'\
              '<p>Hey, if you\'re searching for Jarvis, '\
              'you\'re in the right place.</p>'\
              '<p>It\'s almost here.</p>'\
              'The webhook is ---> <a href="/webhook">HERE</a>'
    return content


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

#    print("Request:")
#    print(json.dumps(req, indent=4))

    res = process_request(req)
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


def process_request(req):
    print("processing Request")
    res = None
    if req.get("result").get("action") == "weatherForecast":
        print("process weather request")
        res = forecast.make_forecast_webhook_result(req)
    if req.get("result").get("action") == "productInfo":
        print("process openfood request")
        res = openfood.make_product_info_webhook_result(req)
    if req.get("result").get("action") == "storeLocation":
        print("process place request")
        res = place.make_store_location_webhook_result(req)
    if req.get("result").get("action") == "setAllergies":
        print("process setAllergies request")
        res = allergy.set_allergies_intent(req)
    if req.get("result").get("action") == "getAllergies":
        print("process getAllergies request")
        res = allergy.get_allergies_intent(req)

    print('========== RES ==========')
    print(res)
    return res


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=True, port=port, host='0.0.0.0')
