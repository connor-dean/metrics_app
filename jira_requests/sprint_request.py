from .request_utils import RequestUtils
import json
import requests


class SprintRequest:

    def make_sprint_request(self):
        utils = RequestUtils()

        user_data = utils.get_user_config_data()
        username = user_data["username"]
        auth_token = user_data["authToken"]

        query_data = utils.get_query_data()
        api = query_data["sprintApi"]

        response = requests.get(api, auth=(username, auth_token)).json()

        with open('data_sprint.json', 'w') as outfile:
            json.dump(response, outfile)

        return response
