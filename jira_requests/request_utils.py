import os
import json

class RequestUtils:
    
    def get_user_config_data(self):
        config_path = os.path.abspath("./configs/user_config.json")
        user_data = self.get_user_params_file(config_path)
        return user_data

    def get_query_data(self):
        param_path = os.path.abspath("./configs/query_config.json")
        query_data = self.get_user_params_file(param_path)
        return query_data

    def get_user_params_file(self, config_file):
        with open(config_file) as config:
            data = json.load(config)

        return data