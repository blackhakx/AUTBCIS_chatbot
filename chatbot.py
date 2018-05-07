from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from random import shuffle
import sys
from wit import Wit

access_token = "KHZTPELNAGRKEYLCM3RLQSFLXBNXG6ZP"


def first_entity_value(entities, entity):
    if entity not in entities:
        return None
    val = entities[entity][0]['value']
    if not val:
        return None
    return val['value'] if isinstance(val, dict) else val


def major_papers(major):
    return "major"


def handle_message(response):
    entities = response['entities']
    major = first_entity_value(entities, 'major')
    greetings = first_entity_value(entities, 'greetings')

    if major:
        print(major)
        return major_papers(major)
    elif greetings:
        return 'Hello, how can I help you?'
    else:
        return 'I do not understand you'


client = Wit(access_token=access_token)
client.interactive(handle_message=handle_message)