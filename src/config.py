import yaml


def get_config(file_name="config.yml"):
    with open(file_name, 'r') as ymlfile:
        cfg = yaml.safe_load(ymlfile)

        return cfg
