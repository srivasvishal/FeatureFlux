import os
import yaml

class Config:
    def __init__(self, config_file=None):
        self.env = os.environ.get("FEATUREFLUX_ENV", "local")
        self.config = {}
        if config_file:
            with open(config_file, "r") as f:
                self.config = yaml.safe_load(f)
    
    def get(self, key, default=None):
        return self.config.get(key, os.environ.get(key, default))