from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from random import shuffle
import sys
from wit import Wit

access_token = "KHZTPELNAGRKEYLCM3RLQSFLXBNXG6ZP"


pre_req = {
    'Programming 2': 'Programming 1',
    'Data & Process Modelling': 'Programming 1',
    'Logical Database Design': 'Programming 1 or Programming for Engineering Applications',
    'Programming Design & Construction': 'Programming 2',
    'Software Development Practice': 'Programming Design & Construction or Data Structures & Algorithms',
    'Operating Systems': 'Foundations of IT Infrastructure and choose between Programming 2 or Data Structures & Algorithms',
    'Physical Database Design': 'Programming 2 and Logical Database Design',
    'Software Engineering': 'Program Design & Construction or Data Structures & Algorithms',
    'Web Development':  'Program Design & Construction',
    'Distributed & Mobile Systems': 'Algorithm Design & Analysis',
    'Research & Development Project': 'IT Project Management & Software Development Practice'
}

co_req = {
    'Programming Design & Construction': 'IT Project Management',
    'Software Development Practice': 'Data & Process Modelling'
}


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


def get_co_req(paper):
    coreq = co_req.get(paper)
    if coreq is None:
        return 'There is no co-requisite for ' + paper
    else:
        return coreq


def get_co_req_pre_req(paper):
    coreq = co_req.get(paper)
    prereq = pre_req.get(paper)
    if prereq is None and coreq is None:
        return 'There is no pre-requisite and co-requisite for ' + paper
    elif coreq is not None and prereq is None:
        return 'co-requisite: ' + coreq + '\npre-requisite: none'
    elif coreq is None and prereq is not None:
        return 'co-requisite: none \npre-requisite: ' + prereq
    else:
        return 'co-requisite: ' + coreq + '\npre-requisite: ' + prereq


def get_pre_req(paper):
    prereq = pre_req.get(paper)
    if prereq is None:
        return 'There is no pre-requisite for ' + paper
    else:
        return prereq


def eligible(paper):
    prereq = pre_req.get(paper)
    if prereq is not None:
        return 'If you have taken ' + prereq + ' then you can take ' + paper
    else:
        return 'You are able to take ' + paper


def user_intent(entities, intent):
    # know what user intent
    if intent == 'study':
        major = first_entity_value(entities, 'major')
        return major_papers(major)
    elif intent == 'co-req':
        paper = first_entity_value(entities, 'paper')
        return get_co_req(paper)
    elif intent == 'pre-req':
        paper = first_entity_value(entities, 'paper')
        return get_pre_req(paper)
    elif intent == 'pre-req_co-req':
        paper = first_entity_value(entities, 'paper')
        return get_co_req_pre_req(paper)
    elif intent == 'eligibility':
        paper = first_entity_value(entities, 'paper')
        return eligible(paper)


def handle_message(response):
    entities = response['entities']
    intent = first_entity_value(entities, 'intent')
    greetings = first_entity_value(entities, 'greetings')
    bye = first_entity_value(entities, 'bye')
    print(intent, entities)
    # Check if user intent is defined or wit.ai made entities
    if intent:
        return user_intent(entities, intent)
    elif greetings:
        return 'Hello, how can I help you?'
    elif bye:
        exit(1)
    else:
        return 'I do not understand you.'


client = Wit(access_token=access_token)
client.interactive(handle_message=handle_message)