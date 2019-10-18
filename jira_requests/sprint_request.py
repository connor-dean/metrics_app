from .request_utils import RequestUtils
import json
import requests

class SprintRequest:
    # curl https://hudl-jira.atlassian.net/rest/agile/1.0/board/30/sprint

    def make_sprint_request(self):
        utils = RequestUtils()

        user_data = utils.get_user_config_data()
        username = user_data["username"]
        auth_token = user_data["authToken"]

        query_data = utils.get_query_data()
        api = query_data["sprintApi"]

        # params = (
        #     ('jql', jql),    
        # )

        #response = requests.get(api, params=params, auth=(username, auth_token)).json()
        response = requests.get(api, auth=(username, auth_token)).json()

        with open('data_sprint.json', 'w') as outfile:
            json.dump(response, outfile)

        print(response)

        return response