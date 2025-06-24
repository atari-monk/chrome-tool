import time
from colorama import Fore, Style
from chatgpt.config.code_block_config import CodeBlockConfig
from chatgpt.config.prompt_config import PromptConfig
from chatgpt.config.chatgpt_config import ChatGPTConfig
from chatgpt.chatgpt_automation import (
    save_code_block,
    send_prompt,
)
from chrome_automation import open_chrome_with_profile
from colorama_utils import color_print
from selenium import webdriver


def open_chatgpt_session(config: ChatGPTConfig) -> webdriver.Chrome | None:
    color_print(f"Initializing Chrome with profile...\n", Fore.RED, style=Style.BRIGHT)
    return open_chrome_with_profile(config)


def send_chatgpt_prompt(config: PromptConfig) -> None:
    color_print(f"Sending Prompt..\n", Fore.RED, style=Style.BRIGHT)
    if config.printPrompt:
        print(config.prompt)
    if config.use_delay:
        print(f"delay of {config.delay_seconds}...")
        time.sleep(config.delay_seconds)
        send_prompt(config)
    else:
        input("Enter to send prompt...") 
        send_prompt(config)


def save_chatgpt_code_block(config: CodeBlockConfig):
    color_print(f"Saving Response..\n", Fore.RED, style=Style.BRIGHT)
    response = ''
    if config.use_delay:
        print(f"delay of {config.delay_seconds}...")
        time.sleep(config.delay_seconds)
        response = save_code_block(config)
    else:
        input("Enter to save...") 
        response = save_code_block(config)
    if config.printResponse:
        print("Response:")
        print(response)
    return response
