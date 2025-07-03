from pathlib import Path
from chrome_tool.code_block_config import CodeBlockConfig
from chrome_tool.prompt_config import PromptConfig
from chrome_tool.chatgpt_cli import (
    open_chatgpt_session,
    save_chatgpt_code_block,
    send_chatgpt_prompt,
)
from chrome_tool.chatgpt_config import ChatGPTConfig


class ChatGPTAgent:
    def __init__(self):
        self.driver = None

    def open(self):
        if self.driver is not None:
            self.driver.quit()
        self.driver = open_chatgpt_session(
            ChatGPTConfig(
                page="https://chat.openai.com/",
                detach=True))

    def close(self):
        if self.driver is not None:
            self.driver.quit()
            self.driver = None

    def send_prompt(self, prompt:str):
        if self.driver is None:
            raise Exception("ChatGPT session is not open.")
        send_chatgpt_prompt(PromptConfig(driver=self.driver, prompt=prompt))

    def save_code(self, output_file_path: Path) -> str | None:
        if self.driver is None:
            raise Exception("ChatGPT session is not open.")
        return save_chatgpt_code_block(CodeBlockConfig(driver=self.driver, output_file_path=output_file_path, overwrite=True))