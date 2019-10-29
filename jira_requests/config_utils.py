import os
import json


class ConfigUtils:

    def get_user_config_data(self):
        try:
            config_path = os.path.abspath('./configs/user_config.json')
            user_data = self.get_user_params_file(config_path)
        except:
            print('Unable to locate the user_config.json file. Do you have one created in the root of the directory?')

        return user_data

    def get_query_config_data(self):
        try:
            param_path = os.path.abspath('./configs/query_config.json')
            query_data = self.get_user_params_file(param_path)
        except:
            print('Unable to locate the query_config.json file. Do you have one created in the root of the directory?')

        return query_data

    def get_user_params_file(self, config_file):
        with open(config_file) as config:
            data = json.load(config)

        return data
