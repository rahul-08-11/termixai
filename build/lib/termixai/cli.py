import argparse
import os
import sys
import asyncio
import json
from platformdirs import user_config_dir
from termixai.inface import ChatUI
import getpass


APP_NAME = "termixai"
CONFIG_DIR = user_config_dir(APP_NAME)
os.makedirs(CONFIG_DIR, exist_ok=True)

def setup_model_config():
    CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")
    if os.path.exists(CONFIG_PATH):
        print("Config file already exists.")
    else:
        with open(CONFIG_PATH, "w") as f:
            json.dump({"models":{}}, f)
    
    print("Select a Model: ")
    print("1. OpenAI")
    print("2. Gemini")
    print("3. Azure OpenAI")
    choice = input("Enter your choice (1-3): ")

    selection_model = {}
    if choice == "1":
        api_key = getpass.getpass("Enter your OpenAI API key: ")
        model_name = input("Enter your OpenAI model name: ")
        selection_model[model_name] = {"provider": "openai", "api_key": api_key, "model_name": model_name}
    elif choice == "2":
        api_key = getpass.getpass("Enter your Gemini API key: ")
        model_name = input("Enter your Gemini model name: ")
        selection_model[model_name] = {"provider": "gemini", "api_key": api_key, "model_name": model_name}
    elif choice == "3":
        api_key = getpass.getpass("Enter your Azure OpenAI API key: ")
        endpoint = input("Enter your Azure OpenAI endpoint: ")
        model_name = input("Enter your Azure OpenAI deployment name: ")
        selection_model[model_name] = {"provider": "azure", "api_key": api_key, "endpoint": endpoint, "model_name": model_name}
    else:
        print("Invalid choice.")

    ## read
    existing_config = None
    with open(CONFIG_PATH, "r") as f:
        existing_config = json.load(f)

    ## append new selection model into models key

    existing_config["models"].update(selection_model)

    ## save new model
    with open(CONFIG_PATH, "w") as f:
        json.dump(existing_config, f, indent=4)
 
    print(f"Configuration saved to {CONFIG_PATH}")


def main():
    parser = argparse.ArgumentParser(
        description="🧠 AI Shell Assistant - interact with your Linux system using natural language."
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # config command
    subparsers.add_parser("config", help="Configure your AI model provider")

    # chat command
    subparsers.add_parser("chat", help="Start chat with AI")


    args = parser.parse_args()

    if args.command == "config":
        setup_model_config()
    elif args.command == "chat":
        ChatUI().run()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
