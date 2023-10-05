import yaml


with open("./config.yml") as yaml_file:
    yaml_data = yaml.safe_load(yaml_file)

SECRET_KEY = yaml_data["jwt"]["SECRET_KEY"]
ALGORITHM = yaml_data["jwt"]["ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = yaml_data["jwt"]["ACCESS_TOKEN_EXPIRE_MINUTES"]
PEPPER = yaml_data["jwt"]["PEPPER"]
