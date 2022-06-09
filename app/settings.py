import yaml

def read_yaml(self, file_path="config.yml"):
        with open(file_path, "r") as f:
            return yaml.safe_load(f)