# Jarvis the nutritionist - made with API.ai

This is a Python Api.ai webhook. More info could be found here:
[Api.ai Webhook](https://docs.api.ai/docs/webhook)

This service communicate with an Api.ai agent related to Jarvis. The service packs the result in the Api.ai webhook-compatible response JSON and returns it to Api.ai.


## Deployment

This webhook is automatically deployed on Heroku when pushing to `master`.

## Run python locally

To test a feature before deploying it, here's how to do:

1) Create a new Api.ai agent and import the content from the production-ready one.

2) Install [ngrok](https://ngrok.com) on your machine.

3) Run `ngrok`. It will create a tunnel from your localhost to a specific IP address. 

    `./ngrok http 5000`

4) Link your Api.ai agent to your specific IP. Go to the "Fulfillment" tab on the Api.ai interface and copy your IP + "/webhook". For example:

    `https://123456789.ngrok.io/webhook`

5) Run the webhook on your localhost:

    `python app.py`


## Link local run with API.ai instance and Facebook Page

1) Make sure step '3' and '4' of previous chapter have been done properly.

2) From your test application in your [Facebook developer page](https://developers.facebook.com), click on 'Messenger' or add new product -> Messenger if not present yet.

3) In 'Token Generation', select the Facebook page you want to link with your local run.

4) Copy the Page Access Token

5) In your API.ai agent, in 'Integrations', chose 'Facebook Messenger', and paste the page access token in the corresponding area

6) Use "api_token" as verify token

7) Copy the Callback URL of your agent

8) Back on your Facebook developer page, select Messenger, and under Webhooks, subscribe webhooks to your page.

9) Add product 'Webhooks' if not present yet. Select 'Webhooks' and edit the subscription of the 'Page'.

10) Use the Api.ai agent's Callback URL, and "api_token" as verify token


### Python 3.x virtualenv creation

Create a virtual environment with Python 3.5 (or 3.6)

	virtualenv -p /usr/bin/python3.5 venv

Enter the virtual environment

	source venv/bin/activate

Install dependencies

	pip install -r requirements.txt

Copy `.env.dist` to `.env` and fill in the variables with real values. Then export the environment variables

	export $(cat .env)

Now you can run the webhook with `python app.py`. When you want to exit the virtualenv, just type:

    deactivate
