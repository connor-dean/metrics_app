from .config_utils import ConfigUtils
import requests
import json


class TicketRequest:

    def make_ticket_request(self, query):
        utils = ConfigUtils()

        user_data = utils.get_user_config_data()
        username = user_data['username']
        auth_token = user_data['authToken']

        query_data = utils.get_query_config_data()
        api = query_data['ticketApi']
        jql = query.ticket_jql

        params = (
            ('jql', jql),
        )

        response = requests.get(
            api, params=params, auth=(username, auth_token)).json()

        with open('data_ticket.json', 'w') as outfile:
            json.dump(response, outfile)

        return response
