#!/usr/bin/env python
# coding:utf-8

# Messenger API integration example
# We assume you have:
# * a Wit.ai bot setup (https://wit.ai/docs/quickstart)
# * a Messenger Platform setup (https://developers.facebook.com/docs/messenger-platform/quickstart)
# You need to `pip install the following dependencies: requests, bottle.
#
# 1. pip install requests bottle
# 2. You can run this example on a cloud service provider like Heroku, Google Cloud Platform or AWS.
#    Note that webhooks must have a valid SSL certificate, signed by a certificate authority and won't work on your localhost.
# 3. Set your environment variables e.g. WIT_TOKEN=your_wit_token
#                                        FB_PAGE_TOKEN=your_page_token
#                                        FB_VERIFY_TOKEN=your_verify_token
# 4. Run your server e.g. python examples/messenger.py {PORT}
# 5. Subscribe your page to the Webhooks using verify_token and `https://<your_host>/webhook` as callback URL.
# 6. Talk to your bot on Messenger!

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import requests
import chatbot as chatbot
from sys import argv
from wit import Wit
from bottle import Bottle, request, debug

# Wit.ai parameters
WIT_TOKEN = os.environ.get('KHZTPELNAGRKEYLCM3RLQSFLXBNXG6ZP')
# Messenger API parameters
FB_PAGE_TOKEN = os.environ.get('EAAci4vcHi9gBAAx4dYNmIrSCJeb9Q1jZA6tI5Dif3UemZCHe3tuEZAk5qUiokwcgjDD9BKVMur05bFrQJlPFvmYxejd9azAoxrRPyVTY5ZANgmfagZA5MZBJdN4LGHB6a4cbZCMUONAZCk9yQpEQs4usZBBZAcDb93XHTBUjstGK1dDTkmvPvEpZBedN')
# A user secret to verify webhook get request.
FB_VERIFY_TOKEN = os.environ.get('FEFEWEFE12')

# Setup Bottle Server
debug(True)
app = Bottle()


# Facebook Messenger GET Webhook
@app.get('https://dashing-attraction.glitch.me/webhook')
def messenger_webhook():
    """
    A webhook to return a challenge
    """
    verify_token = request.query.get('hub.verify_token')
    # check whether the verify tokens match
    if verify_token == FB_VERIFY_TOKEN:
        # respond with the challenge to confirm
        challenge = request.query.get('hub.challenge')
        return challenge
    else:
        return 'Invalid Request or Verification Token'


# Facebook Messenger POST Webhook
@app.post('/webhook')
def messenger_post():
    """
    Handler for webhook (currently for postback and messages)
    """
    data = request.json
    if data['object'] == 'page':
        for entry in data['entry']:
            # get all the messages
            messages = entry['messaging']
            if messages[0]:
                # Get the first message
                message = messages[0]
                # Yay! We got a new message!
                # We retrieve the Facebook user ID of the sender
                fb_id = message['sender']['id']
                # We retrieve the message content
                text = message['message']['text']
                # Let's forward the message to Wit /message
                # and customize our response to the message in handle_message
                response = client.message(msg=text, context={'session_id':fb_id})
                handle_message(response=response, fb_id=fb_id)
    else:
        # Returned another event
        return 'Received Different Event'
    return None


def fb_message(sender_id, text):
    """
    Function for returning response to messenger
    """
    data = {
        'recipient': {'id': sender_id},
        'message': {'text': text}
    }
    # Setup the query string with your PAGE TOKEN
    qs = 'access_token=' + FB_PAGE_TOKEN
    # Send POST request to messenger
    resp = requests.post('https://graph.facebook.com/me/messages?' + qs,
                         json=data)
    return resp.content


def handle_message(response, fb_id):
    """
    Customizes our response to the message and sends it
    """
    entities = response['entities']
    intent = chatbot.first_entity_value(entities, 'intent')
    greetings = chatbot.first_entity_value(entities, 'greetings')
    bye = chatbot.first_entity_value(entities, 'bye')
    # Check if user intent is defined or wit.ai made entities
    if intent:
        text =chatbot.user_intent(entities, intent)
    elif greetings:
        text = 'Hello, how can I help you?'
    elif bye:
        text = 'bye'
    else:
        text = 'I do not understand you.'
    # send message
    fb_message(fb_id, text)


# Setup Wit Client
client = Wit(access_token=WIT_TOKEN)

if __name__ == '__main__':
    # Run Server
    app.run(host='0.0.0.0', port=argv[1])