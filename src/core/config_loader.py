import yaml
import os

class ConfigLoader:
    def __init__(self, config_dir="./configs"):
        self.config_dir = config_dir
    
    def load_language_config(self, language_code):
        """Load language-specific configuration"""
        path = os.path.join(
            self.config_dir, 
            "languages", 
            f"{language_code}.yaml"
        )
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def load_default_config(self):
        """Load default configuration"""
        path = os.path.join(self.config_dir, "default.yaml")
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
