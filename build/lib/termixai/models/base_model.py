import subprocess
import json
import os
import pkg_resources

class BaseModel:


    def __init__(self):
        self.system_message = """You are a smart AI assistant embedded in a Linux terminal. You interact with the user in natural language and use shell commands behind the scenes to answer their questions or perform tasks.

                                Your behavior:
                                - Understand the user's intent and determine the safest, most appropriate Linux command(s) to satisfy the request.
                                - Use the result of the command(s) to provide a clear, human-friendly answer.
                                - If the request is too vague, unsafe, or would involve destructive actions (like `rm`, `dd`, `mkfs`, `shutdown`, etc), reply politely with an explanation and do not run any command.
                                - Do not mention you're using shell commands unless the user asks explicitly.
                                - Do not just paste the raw output. Instead, summarize the key points in plain English and explain what it means.
                                - Format your answer properly to make it suitable for terminal display.Do not include any markdown or code block tags.
                                - Interpret User's input and help them with their queries by taking action if needed.
                                Always prioritize safety and clarity. Speak like a helpful Linux power user — calm, informative, and brief.
                                
                          """


    async def chat(self, messages):
        pass


    async def load_tools(self, tools_directory=None):
        if tools_directory is None:
            # Get the absolute path to the tools directory within the package
            tools_directory = pkg_resources.resource_filename('termixai', 'models/tools')
        
        tools = []
        for file_name in os.listdir(tools_directory):
            if file_name.endswith(".json"):
                with open(os.path.join(tools_directory, file_name), "r") as tool_file:
                    tools.append(json.load(tool_file))
        return tools

    async def load_tool_response(self, response):
        pass

    ## tool
    async def run_shell_process(self, command: str):
        process = subprocess.Popen(
            command, shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
        )
        return process