import yaml


class InitializePipeline:
    def __init__(self, config_file_path):
        self.config_file_path = config_file_path
        self.config_file = self.load_config()

    def load_config(self):
        with open(self.config_file_path, 'r') as file:
            config = yaml.safe_load(file)

        return config

    def get_config(self):
        return self.config_file
