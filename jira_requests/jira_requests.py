import json
import os
import requests


def make_sprint_request():
    user_data = get_user_config_data()
    username = user_data['username']
    auth_token = user_data['authToken']

    query_data = get_query_config_data()
    project_num = query_data['projectNum']
    api = f'https://hudl-jira.atlassian.net/rest/agile/1.0/board/{project_num}/sprint'

    try:
        response = requests.get(api, auth=(username, auth_token)).json()
        with open('data_sprint.json', 'w') as outfile:
            json.dump(response, outfile)
    except:
        print(
            'Something went wrong requesting sprint information. Is your board # correct?')

    return response


def make_ticket_request(query):
    user_data = get_user_config_data()
    username = user_data['username']
    auth_token = user_data['authToken']

    query_data = get_query_config_data()
    api = query_data['ticketApi']
    jql = query.ticket_jql

    params = (
        ('jql', jql),
    )

    try:
        response = requests.get(
            api, params=params, auth=(username, auth_token)).json()
        with open('data_ticket.json', 'w') as outfile:
            json.dump(response, outfile)
    except:
        print(
            'Something went wrong requesting ticket information. Is your ticket API url correct?')

    return response


def get_user_config_data():
    try:
        config_path = os.path.abspath('./configs/user_config.json')
        user_data = get_user_params_file(config_path)
    except:
        print('Unable to locate the user_config.json file. Do you have one created in the root of the directory?')

    return user_data


def get_query_config_data():
    try:
        param_path = os.path.abspath('./configs/query_config.json')
        query_data = get_user_params_file(param_path)
    except:
        print('Unable to locate the query_config.json file. Do you have one created in the root of the directory?')

    return query_data


def get_user_params_file(config_file):
    with open(config_file) as config:
        data = json.load(config)

    return data
