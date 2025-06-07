import os
import json
from platformdirs import user_config_dir

CONFIG_DIR = user_config_dir("ai_assist")
APP_NAME = "ai_assist"
CONFIG_DIR = user_config_dir(APP_NAME)
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")



# 👇 Add this before writing the file
os.makedirs(CONFIG_DIR, exist_ok=True)
def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {"models": {}}  # Return an empty config if file doesn't exist
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def get_model_config(model_name):
    config = load_config()
    profiles = config.get("models", {})
    if model_name not in profiles:
        raise ValueError(f"Model '{model_name}' not found.")
    return profiles[model_name]
