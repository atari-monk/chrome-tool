from pathlib import Path
from chrome_tool.code_block_config import CodeBlockConfig
from chrome_tool.prompt_config import PromptConfig
from chrome_tool.chatgpt_config import ChatGPTConfig
from chrome_tool.chrome_automation import open_chrome_with_profile
from chrome_tool.chatgpt_automation import save_code_block, send_prompt


class ChatGPTAgent:
    def __init__(self):
        self.driver = None

    def open(self):
        if self.driver is not None:
            self.driver.quit()
        self.driver = open_chrome_with_profile(
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
        send_prompt(PromptConfig(driver=self.driver, prompt=prompt))

    def save_code(self, output_file_path: Path) -> str | None:
        if self.driver is None:
            raise Exception("ChatGPT session is not open.")
        return save_code_block(CodeBlockConfig(driver=self.driver, output_file_path=output_file_path, overwrite=True))