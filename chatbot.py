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
    init_reply = 'That is great! Here is the programme for '
    if major == 'Analytics':
        return init_reply + major + ':\nhttps://www.aut.ac.nz/study/study-options/engineering-computer-and-mathematical-sciences/courses/bachelor-of-computer-and-information-sciences/analytics-major'
    elif major == "Software Development":
        return init_reply + major + ':\nhttps://autdev.aut.ac.nz/study/study-options/engineering-computer-and-mathematical-sciences/courses/bachelor-of-computer-and-information-sciences/software-development-major'
    elif major == 'IT Service Sciences':
        return init_reply + major + ':\nhttps://autdev.aut.ac.nz/study/study-options/engineering-computer-and-mathematical-sciences/courses/bachelor-of-computer-and-information-sciences/it-service-science-major'
    elif major == 'Computational Intelligence':
        return init_reply + major + ':\nhttps://autdev.aut.ac.nz/study/study-options/engineering-computer-and-mathematical-sciences/courses/bachelor-of-computer-and-information-sciences/computational-intelligence-major'
    elif major == 'Network & Security':
        return init_reply + major + ':\nhttps://autdev.aut.ac.nz/study/study-options/engineering-computer-and-mathematical-sciences/courses/bachelor-of-computer-and-information-sciences/networks-and-security-major'
    elif major == 'Computer Science':
        return init_reply + major + ':\nhttps://autdev.aut.ac.nz/study/study-options/engineering-computer-and-mathematical-sciences/courses/bachelor-of-computer-and-information-sciences/computer-science-major'
    elif major is None:
        return 'What do you want to study?'
    else:
        return 'AUT do not offer that programme'


def user_intent(entities, intent):
    # know what user intent
    if intent == 'study':
        major = category = first_entity_value(entities, 'major')
        return major_papers(major)


"""
def handle_message(response):
    entities = response['entities']
    #major = first_entity_value(entities, 'major')
    greetings = first_entity_value(entities, 'greetings')
    intent = first_entity_value(entities, 'intent')
    if major:
        return major_papers(major)
    elif greetings:
        return 'Hello, how can I help you?'
    else:
        return 'I do not understand you'
"""


def handle_message(response):
    entities = response['entities']
    intent = first_entity_value(entities, 'intent')
    greetings = first_entity_value(entities, 'greetings')
    print(intent, entities)
    # Check if user intent is defined or wit.ai made entities
    if intent:
        return user_intent(entities, intent)
    elif greetings:
        return 'Hello, how can I help you?'
    else:
        return 'I do not understand you.'


client = Wit(access_token=access_token)
client.interactive(handle_message=handle_message)