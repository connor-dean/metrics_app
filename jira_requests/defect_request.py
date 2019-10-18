from .request_utils import RequestUtils
import requests
import json

class DefectRequest:

    def make_defect_request(self):
        utils = RequestUtils()

        user_data = utils.get_user_config_data()
        username = user_data["username"]
        auth_token = user_data["authToken"]

        query_data = utils.get_query_data()
        api = query_data["defectApi"]
        jql = query_data["defectJql"]

        params = (
            ('jql', jql),    
        )

        response = requests.get(api, params=params, auth=(username, auth_token)).json()

        with open('data_defect.json', 'w') as outfile:
            json.dump(response, outfile)

        return response
