import json


class ConfigurationManager:
    def __init__(self, file="config.json"):
        self._config_file = file
        with open(self._config_file, "r") as config_file:
            self._config = json.load(config_file)

    @property
    def twilio_token(self):
        return self._config["twilio_config"]["auth_token"]

    @property
    def twilio_sid(self):
        return self._config["twilio_config"]["account_sid"]

    @property
    def twilio_source(self):
        return self._config["twilio_config"]["source"]
