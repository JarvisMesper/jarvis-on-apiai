# Jarvis the nutritionist - made with API.ai

This is a Python Api.ai webhook. More info could be found here:
[Api.ai Webhook](https://docs.api.ai/docs/webhook)

This service communicate with an Api.ai agent related to Jarvis. The service packs the result in the Api.ai webhook-compatible response JSON and returns it to Api.ai.

## Deployment

This webhook is automatically deployed on Heroku when pushing to `master`.

## Run locally

To test a feature before deploying it, here's how to do:

1) Create a new Api.ai agent and import the content from the production-ready one.

2) Install [ngrok](https://ngrok.com) on your machine.

3) Run `ngork`. It will create a tunnel from your localhost to a specific IP address. 

    `./ngrok http 5000`

4) Link your Api.ai agent to your specific IP. Go to the "Fulfillment" tab on the Api.ai interface and copy your IP + "/webhook". For example:

    `https://123456789.ngrok.io/webhook`

5) Run the webhook on your localhost:

    `python app.py`


### Python 3.x virtualenv creation

Create a virtual environment with Python 3.5 (or 3.6)

	virtualenv -p /usr/bin/python3.5 venv

Enter the virtual environment

	source venv/bin/activate

Install dependencies

	pip install -r requirements.txt

Export environment variables

	export $(cat .env)

Now you can run the webhook with `python app.py`. When you want to exit the virtualenv, just type:

    deactivate
