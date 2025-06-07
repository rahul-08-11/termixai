
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
from azure.ai.inference.models import ToolMessage ,AssistantMessage # Needed to send tool result
from termixai.models.base_model import BaseModel
from colorama import Fore

class AzureOpenAIModel(BaseModel):
    def __init__(self, provider: str, api_key: str, endpoint: str, model_name: str):
        ## Initialize the Azure OpenAI model Client
        super().__init__()
        self.model = ChatCompletionsClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(api_key),
            
        )
        self.deployment_name = model_name
        self.provider = provider



    async def chat(self, prompt: str, memory : list) -> str:
        # Initial request to model
   
        response = self.model.complete(
            messages = [SystemMessage(content=self.system_message)] + memory + [UserMessage(content=prompt)],
            model=self.deployment_name,
            temperature=0.7,
            top_p=1.0,
            tools=[
                {
                    "id": "terminal_tool",
                    "type": "function",
                    "function": {
                        "name": "run_shell_command",
                        "description": "A tool to execute terminal commands and return results.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "command": {
                                    "type": "string",
                                    "description": "The terminal command to execute."
                                },
                                "command_description": {
                                    "type": "string",
                                    "description": "A short description  what the command does."
                                }
                            
                            },
                            "required": ["command"]
                        }
                    }
                }
            ] ,
            
        )

        return response
    

    async def create_tool_msg(self, tool_data : dict):
        tool_messages = []
        for tool_id, tool_output in tool_data.items():
            # Create a ToolMessage for each tool call
            tool_messages.append(
                ToolMessage(
                    tool_call_id=tool_id,
                    content=tool_output
                )
            )
        return tool_messages
    
    async def send_tool_msg(self, original_prompt: str, tool_messages : list, tool_calls):

        messages=[
                    SystemMessage(content=self.system_message), 
                    UserMessage(content=original_prompt)
                ]
          # Append assistant tool call as message
        messages.append(
            AssistantMessage(
                tool_calls=tool_calls,
                content=None
            )
        )
        messages.extend(tool_messages)

        # Follow-up ask model to respond with results
        followup_response = self.model.complete(
            messages=messages,
            model=self.deployment_name,
            temperature=0.7,
            top_p=1.0,
        )
        final_message = followup_response.choices[0].message.content

        return final_message.strip()
    
