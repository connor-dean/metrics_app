from .config_utils import ConfigUtils
import json
import requests


class SprintRequest:

    def make_sprint_request(self):
        utils = ConfigUtils()
        user_data = utils.get_user_config_data()
        username = user_data['username']
        auth_token = user_data['authToken']

        query_data = utils.get_query_config_data()
        project_num = query_data['projectNum']
        api = 'https://hudl-jira.atlassian.net/rest/agile/1.0/board/{project_num}/sprint'.format(
            project_num=project_num)

        try:
            response = requests.get(api, auth=(username, auth_token)).json()
            with open('data_sprint.json', 'w') as outfile:
                json.dump(response, outfile)
        except:
            print(
                'Something went wrong requesting sprint information. Is your board # correct?')

        return response
