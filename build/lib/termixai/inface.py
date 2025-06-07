from textual import on, work
from textual.app import App, ComposeResult
from textual.widgets import Header, Input, Footer, Markdown
from textual.containers import VerticalScroll
import asyncio
import logging
from textual.logging import TextualHandler
from textual.widgets import Static, Button, Select
from textual.containers import Horizontal, Vertical
from textual.message import Message
import subprocess
import json
import os
import sys
# sys.path.append("")  # Adjust path to import termixai modules
from termixai.utils.config import load_config,get_model_config
from termixai.model_factory import ModelFactory

logging.basicConfig(
    level="INFO",
    handlers=[TextualHandler()],
)

class Prompt(Markdown):
    """Widget to display user prompts in Markdown."""
    BORDER_TITLE = "You"


class ChatUIMessage(Markdown):
    """Widget to display AI responses, with a border title."""
    BORDER_TITLE = "System"

class Response(Markdown):
    """Widget to display AI responses, with a border title."""
    BORDER_TITLE = "TermiXAI"

class CommandApprovalRequested(Message):
    """Fired when the user clicks Approve or Cancel on a command approval."""
    def __init__(self, sender, command: str, approved: bool , tool_id : str) -> None:
        super().__init__()
        self.sender = sender
        self.command = command
        self.approved = approved
        self.tool_id = tool_id

class CommandApproval(Static):
    """A little approval form: "Run `…` ?" + [Approve] [Cancel]"""

    def __init__(self, command: str,command_description: str, tool_id : str) -> None:
        super().__init__()
        self.command = command
        self.tool_id = tool_id
        self.command_description = command_description

    def compose(self):
        # Use Vertical layout with better structure
        with Vertical():
            yield Static(f"[AI] I'd like to run `{self.command}` - {self.command_description}", id="command_text")
            # Use Horizontal layout for buttons
            with Horizontal():
                yield Button("Approve", id="approve", variant="success")
                yield Button("Cancel", id="cancel", variant="error")

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """When either button is clicked, fire a Message back to the App."""
        approved = (event.button.id == "approve")
        # Emit a higher‐level message with the result
        self.post_message(CommandApprovalRequested(self, self.command, approved, tool_id=self.tool_id))

class ChatUI(App):
    """A terminal chat app that role-plays the 'Mother' AI from the Aliens movies."""
    AUTO_FOCUS = "Input"
    THEME = "nord"
    _pending_call = None
    _original_prompt= None
    _response = None
    _active_model_name = None
    _models = list(load_config()["models"].keys())
    _active_model_instance = None
    _pending_tool_approvals: dict = {}
    _total_tool_calls: int = 0
    _multiple_tool_call_data = {}
    _tool_calls = None
    _memory_context : list = []
    _input_field_widget = None
    TITLE = "TermiXAI Chat UI"

    CSS = """
    Prompt {
        background: $primary 10%;
        color: $text;
        margin: 1 1 1 3; 
        margin-right: 8;
        padding: 1 2 0 2;
    }

    Response {
        border: wide $success;
        background: $success 10%;
        color: $text;
        margin: 1 1 1 3; 
        margin-left: 8;
        padding: 1 2 0 2;
    }

    ChatUIMessage {
        background: $secondary 10%;
        color: $text;
        padding: 0 1;
        margin: 1 60 1 60;
        border: solid $secondary 5%;
        align-horizontal: center;
    }

    CommandApproval {
        border: wide $success;
        background: $success 10%;
        color: $text;
        margin: 1 1 1 3; 
        margin-left: 8;
        padding: 1 2;
        height: auto;  /* Changed from fixed height */
        min-height: 6;  /* Increased minimum height */
    }

    CommandApproval Vertical {
        height: auto;  /* Changed from fixed height */
        padding: 0;
    }

    CommandApproval Static {
        height: auto;  /* Allow text to wrap if needed */
        margin: 0 0 1 0;
    }

    CommandApproval Horizontal {
        height: auto;  /* Changed from fixed height */
        align: left middle;
    }

    CommandApproval Button {
        background: $warning;
        color: $text;
        border: solid $warning;
        margin: 0 1 0 0;
        height: 3;
        min-width:13;
        max-width: 15;
        padding: 0 1;
        text-align: center;
    }

    /* Add hover effect for better UX */
    CommandApproval Button:hover {
        background: $warning 80%;
    }

    /* Style the approve button differently */
    CommandApproval Button#approve {
        background: $success;
        border: solid $success;
        color: $text;
    }

    CommandApproval Button#approve:hover {
        background: $success 80%;
    }

    /* Style the cancel button differently */
    CommandApproval Button#cancel {
        background: $error;
        border: solid $error;
        color: $text;
    }

    CommandApproval Button#cancel:hover {
        background: $error 80%;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield Select(
            [(model, model) for model in self._models],
            prompt="Choose model",
            id="model_select"
        )

        with VerticalScroll(id="chat-view"):
            pass

        yield Input(placeholder="How can I help you?",id="input_field")
        yield Footer()

    @on(Select.Changed, "#model_select")
    async def model_selected(self, event: Select.Changed) -> None:
        self._active_model_name = event.value
        ## create model instance 
        self._active_model_instance = await ModelFactory.create(self._active_model_name)

    @on(Input.Submitted)
    async def on_input(self, event: Input.Submitted) -> None:
        self._input_field_widget = self.query_one("#input_field", Input)
        self._input_field_widget.disabled = True

        """Handle user pressing Enter: display prompt, prepare response bubble, and fire off the worker."""
        self._memory_context.append({"role": "user", "content": event.value})
        # Trim memory to last 5
        self._memory_context = self._memory_context[-5:]
        chat_view = self.query_one("#chat-view")
        event.input.clear()
        if self._active_model_instance is None:
            await chat_view.mount(ChatUIMessage("Please select a model first"))
            return
        await chat_view.mount(Prompt(event.value))
        self._original_prompt = event.value
        self.send_prompt(event.value)

    @work(thread=True)
    async def send_prompt(self, prompt: str) -> None:
        # 1) call your Azure model "dry" to get tool_calls
        self._response = await self._active_model_instance.chat(prompt = prompt, memory = self._memory_context)
        logging.info(f"Response: {self._response}")
        if self._active_model_instance.provider == "azure":
            ## check for any tool invokation by AI
            self._tool_calls = getattr(self._response.choices[0].message, "tool_calls", None)
            logging.info(f"Tool calls: {self._tool_calls}")
            self._total_tool_calls = len(self._tool_calls) if self._tool_calls else 0
            if self._tool_calls:
                self._multiple_tool_calls =  True if len(self._tool_calls) > 1 else False
                for tool_call in self._tool_calls:
                    function_name = tool_call.function.name
                    tool_id = tool_call.id
                    logging.info(f"Tool call detected: {function_name} (id={tool_id})")
                    arguments = json.loads(tool_call.function.arguments)
                    if function_name == "run_shell_command":
                        command = arguments["command"]
                        command_description = arguments.get("command_description", "No description provided")
                        self.call_from_thread(
                            self.query_one("#chat-view").mount,
                            CommandApproval(command,command_description, tool_id)
                        )
                    self._pending_tool_approvals[tool_id] = "This command did not run yet"  # Mark as pending
                return 
            
        stream = self._response.choices[0].message.content.strip()

        self._memory_context.append({"role": "assistant", "content": stream})
        self._memory_context = self._memory_context[-5:]

        # 2) mount the response like before
        def create_response_widget():
            resp = Response()
            chat_view = self.query_one("#chat-view")
            chat_view.mount(resp)
            resp.anchor()
            return resp

        resp_widget = self.call_from_thread(create_response_widget)
        collected = ""
        for part in stream:
            collected += part
            self.call_from_thread(resp_widget.update, collected)  # schedule update in main thread
                # 3) Reset state
        self._input_field_widget.disabled = False
        self._original_prompt = None
        return 
        

    @work(thread=True)
    async def handle_tool_response(self, original_prompt, tool_call_data, tool_calls):
        toolmsg = await self._active_model_instance.create_tool_msg(tool_call_data)
        ai_response = await self._active_model_instance.send_tool_msg(original_prompt, toolmsg, tool_calls)

        def mount_response():
            resp = Response()
            self.query_one("#chat-view").mount(resp)
            resp.anchor()
            return resp

        resp_widget = self.call_from_thread(mount_response)
        collected = ""
        for part in ai_response:
            collected += part
            self.call_from_thread(resp_widget.update, collected)

            ## enable input widget
        self._input_field_widget.disabled = False

        # Reset state safely
        self._original_prompt = None
        self._multiple_tool_call_data = {}
        self._pending_tool_approvals = {}
        self._tool_calls = None
        self._total_tool_calls = 0

    @on(CommandApprovalRequested)
    async def on_command_approval(self, event: CommandApprovalRequested) -> None:
        chat = self.query_one("#chat-view")
        await event.sender.remove()

        if not event.approved:
            await chat.mount(Static(f"⚠️ Command `{event.command}` cancelled."))
            self._multiple_tool_call_data[event.tool_id]  = "This command did run because it was cancelled by the user"  # Mark as declined
            del self._pending_tool_approvals[event.tool_id]
        else:
            await chat.mount(Static(f"[AI]  Using `{event.command}`"))
            proc = await self._active_model_instance.run_shell_process(event.command)
            output = proc.stdout.read()
            proc.wait()
            self._multiple_tool_call_data[event.tool_id] = output
            del self._pending_tool_approvals[event.tool_id]  # Remove from pending approvals

        # ✅ Check if all tools have responded (approved or declined)
        logging.info(f"Number of pending tool approvals: {len(self._pending_tool_approvals)}")
        logging.info(f"Total tool calls: {self._total_tool_calls}")
        if not len(self._pending_tool_approvals):
            self.handle_tool_response(
                self._original_prompt,
                self._multiple_tool_call_data,
                self._tool_calls
            )
           


if __name__ == "__main__":
    app = ChatUI()
    app.run()