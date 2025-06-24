from pathlib import Path
from chrome_tool.agents.interface.i_chatgpt_agent import IChatGPTAgent


class ChatGPTAgentMock(IChatGPTAgent):
    def __init__(self):
        print("Mock ChatGPTAgentMock initialized")

    def open(self):
        print("Mock Opening ChatGPT session...")

    def close(self):
        print("Mock Closing ChatGPT session...")

    def send_prompt(self, prompt:str, delay_seconds:int=25):
        print(f"Mock Sending prompt (delay {delay_seconds} seconds): {prompt}")

    def save_code(self, output_file_path: Path, delay_seconds:int=1, json: bool = False, overwrite:bool=False) -> str | None:
        print(f"Mock Saving code to {output_file_path} with delay {delay_seconds} seconds, json={json}, overwrite={overwrite}")
        return str(output_file_path)