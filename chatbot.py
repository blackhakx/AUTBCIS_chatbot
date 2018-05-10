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
    'Logical Database Design': 'Programming 1 or Programming for Engineering  Applications',
    'Programming Design & Construction': 'Programming 2',
    'Software Development Practice': 'Programming Design & Construction or Data Structures & Algorithms',
    'Operating Systems': 'Foundations of IT Infrastructure and choose between Programming 2 or Data Structures & Algorithms',
    'Physical Database Design': 'Programming 2 and Logical Database Design',
    'Software Engineering': 'Program Design & Construction or Data Structures & Algorithms',
    'Web Development':  'Program Design & Construction',
    'Distributed & Mobile Systems': 'Algorithm Design & Analysis',
    'Research & Development Project': ''
}

co_req = {
    'Programming Design & Construction': 'IT Project Management',
    'Software Development Practice': 'Data & Process Modelling'
}

core_papers = {
    'COMM501' : 'Applied Communication, ',
    'COMP500' : 'Programming 1, ',
    'COMP501' : 'Computing Technology in Society, ',
    'COMP502' : 'Foundations of IT, ',
    'INFS500' : 'Enterprise Systems, ',
    'COMP503' : 'Programming 2, ',
    'ENEL504' : 'Computer Network Principles (CCNA1), ',
    'STAT500' : 'Applied Statistics, ',
    'MATH501' : 'Differential & Integral Calculus, ',
    'MATH502' : 'Algebra & Discrete Mathematics, ',
    'MATH500' : 'Mathematical Concepts, ',
    'INFS600' : 'Data & Process Modelling, ',
    'INFS601' : 'Logical Database Design, ',
    'COMP600' : 'IT Project Management, ',
    'COMP702' : 'Research and Development Project Part 1, ',
    'COMP703' : 'Research and Development Project Part 2, '
}

softdev_papers = {
    'COMP603' : 'Program Design & Construction, ',
    'COMP602' : 'Software Development Practice, ',
    'COMP604' : 'Operating Systems, ',
    'INFS602' : 'Physical Database Design, ',
    'ENSE701' : 'Software Engineering, ',
    'COMP719' : 'Applied Human Computer Interaction, ',
    'COMP721' : 'Web Development, ',
    'COMP713' : 'Distributed & Mobile Systems, '
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


def get_double_major(double_major):
    user_input = input('Which year are you in? ')
    email = 'To seek for advice on double major, please email: cadvisor@aut.ac.nz'

    # Check years 1, 2 and 3
    if user_input == 'one' or user_input == "1":
        return email
    elif user_input == 'two' or user_input == "2":
        return email
    else:
        return 'I am sorry, you have to either be in year 1 or year 2 to seek for advice in doing a double major'



def get_co_req(paper):
    coreq = co_req.get(paper)
    if coreq is None:
        return 'There is no co-requisite for ' + paper
    else:
        return coreq


def get_co_req_pre_req(paper):
    coreq = co_req.get(paper)
    #print(coreq)
    prereq = pre_req.get(paper)
    #print(prereq)
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


def city_papers(city_campus):
    init_reply = 'The papers available for city campus are: \n'

    year1_sem1_city = 'Year 1, Semester 1: '
    year1_sem1_city_papers = core_papers['COMM501'] + core_papers['COMP500'] + core_papers['COMP501'] + core_papers['COMP502'] + core_papers['INFS500'] + core_papers['COMP503'] + core_papers['ENEL504'] + core_papers['STAT500'] + core_papers['MATH502'] + core_papers['MATH500']
    year1_sem2_city = '\nYear 1, Semester 2: '
    year1_sem2_city_papers = core_papers['COMM501'] + core_papers['COMP500'] + core_papers['COMP501'] + core_papers['COMP502'] + core_papers['INFS500'] + core_papers['COMP503'] + core_papers['ENEL504'] + core_papers['STAT500'] + core_papers['MATH501'] +core_papers['MATH502'] + core_papers['MATH500']
    year1 = year1_sem1_city + year1_sem1_city_papers + year1_sem2_city + year1_sem2_city_papers

    year2_sem1_city = '\nYear 2, Semester 1: '
    year2_sem1_city_papers = core_papers['INFS600'] + core_papers['INFS601'] + core_papers['COMP600'] + softdev_papers['COMP603'] + softdev_papers['COMP602']
    year2_sem2_city = '\nYear 2, Semester 2: '
    year2_sem2_city_papers = core_papers['INFS600'] + core_papers['INFS601'] + core_papers['COMP600'] + softdev_papers['COMP603'] + softdev_papers['COMP602'] + softdev_papers['COMP604'] + softdev_papers['INFS602']
    year2 = year2_sem1_city + year2_sem1_city_papers + year2_sem2_city + year2_sem2_city_papers

    year3_sem1_city = '\nYear 3, Semester 1: '
    year3_sem1_city_papers = softdev_papers['ENSE701'] + softdev_papers['COMP719'] + softdev_papers['COMP721'] + softdev_papers['COMP713'] + core_papers['COMP702'] + core_papers['COMP703']
    year3_sem2_city = '\nYear 3, Semester 2: '
    year3_sem2_city_papers = softdev_papers['ENSE701'] + softdev_papers['COMP719'] + softdev_papers['COMP721'] + softdev_papers['COMP713'] + core_papers['COMP702'] + core_papers['COMP703']
    year3 = year3_sem1_city + year3_sem1_city_papers + year3_sem2_city + year3_sem2_city_papers

    return init_reply + year1 + year2 + year3


def south_papers(south_campus):
    init_reply = 'The papers available for city campus are: \n'

    year1_sem1 = 'Year 1, Semester 1: '
    year1_sem1_papers = core_papers['COMM501'] + core_papers['COMP500'] + core_papers['']


def user_intent(entities, intent):
    # know what user intent4
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
    elif intent == 'double_major':
        double_major = first_entity_value(entities, 'double_major')
        return get_double_major(double_major)
    elif intent == 'city_campus':
        city_campus = first_entity_value(entities, 'city_campus')
        return city_papers(city_campus)


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