from pathlib import Path
from chrome_tool.code_block_config import CodeBlockConfig
from chrome_tool.prompt_config import PromptConfig
from chrome_tool.agent_config import AgentConfig
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pyperclip
import time
from chrome_tool.code_block_config import CodeBlockConfig
from chrome_tool.prompt_config import PromptConfig
from chrome_tool.utils.json import (
    append_json_strings_to_array,
    convert_paths_to_json_safe,
)
from chrome_tool.utils.string import clean_code
from colorama import Fore, Style
from chrome_tool.utils.colorama import color_print
import os
from typing import Any, Optional, cast
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from chrome_tool.utils.url import is_valid_url
from chrome_tool.agent_config import AgentConfig
from colorama import Fore, Style
from chrome_tool.utils.colorama import color_print
from chrome_tool.chrome_profile import ChromeProfile


class Agent:
    def __init__(self):
        self.driver = None

    def open_chrome_with_profile(self, config: AgentConfig = AgentConfig(
                page="https://chat.openai.com/",
                detach=True)) -> None:
        if self.driver is not None:
            self.driver.quit()
        color_print(f"Initializing Chrome with profile...\n", Fore.RED, style=Style.BRIGHT)

        if not is_valid_url(config.page):
            raise ValueError(f"Invalid URL: '{config.page}'. Must include scheme (e.g., https://) and domain.")
        
        if not (profile := self._get_first_chrome_profile()):
            print("No active Chrome profile found")
            return None
        
        print(f"Active Profile: {profile.path}, Profile Directory: {profile.name}")

        options = Options()
        
        options.add_argument(f"user-data-dir={profile.path}")
        options.add_argument(f"profile-directory={profile.name}")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--log-level=3")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        
        experimental_options = cast(Any, options)
        experimental_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        
        if config.detach:
            experimental_options.add_experimental_option("detach", True)

        try:
            service = cast(Any, Service())
            service.creationflags = 0x08000000
            service.quiet = True

            os.environ['WDM_LOG_LEVEL'] = '0'
            os.environ['WDM_PRINT_FIRST_LINE'] = 'False'

            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.get(config.page)
            print(f"Successfully opened: {config.page}")
        except Exception as e:
            print(f"Failed to start Chrome: {str(e)}")

    def _get_first_chrome_profile(self) -> Optional[ChromeProfile]:
        profile_data = [
            (Path("C:/atari-monk/my_chrome_profile"), "Default"),
            (Path("C:/Users/ASUS/AppData/Local/Google/Chrome/User Data"), "Default"),
            (Path("C:/Selenium"), "Profile 2"),
            (Path("C:/Users/atari/AppData/Local/Google/Chrome/User Data"), "Profile 2"),
        ]
        for path, name in profile_data:
            if path.exists():
                return ChromeProfile(path, name)
        return None

    def close(self):
        if self.driver is not None:
            try:
                self.driver.quit()
            except Exception as e:
                print(f"Error while closing driver: {e}")
            finally:
                self.driver = None

    def send_prompt(self, prompt: str) -> bool:
        if self.driver is None:
            raise Exception("ChatGPT session is not open.")
        config = PromptConfig(driver=self.driver, prompt=prompt)
        color_print(f"Sending Prompt..\n", Fore.RED, style=Style.BRIGHT)
        if config.printPrompt:
            print(config.prompt)
        input("Enter to send prompt...") 
        try:
            import pyperclip
            pyperclip.copy(config.prompt)
            
            driver = config.driver
            input_area = driver.find_element(By.ID, config.input_area_id)
            input_area.clear()

            input_area.click()
            
            if driver.name == 'chrome' or driver.name == 'edge':
                input_area.send_keys(Keys.CONTROL, 'v')
            elif driver.name == 'firefox':
                input_area.send_keys(Keys.COMMAND, 'v')
            
            input_area.send_keys(Keys.RETURN)
            print("Prompt sent successfully")
            return True
        except Exception as e:
            print(f"Failed to send prompt: {str(e)}")
            return False
            
    def save_code(self, output_file_path: Path) -> str | None:
        if self.driver is None:
            raise Exception("ChatGPT session is not open.")
        color_print(f"Saving Response..\n", Fore.RED, style=Style.BRIGHT)
        config = CodeBlockConfig(driver=self.driver, output_file_path=output_file_path, overwrite=True)
        input("Enter to save...") 
        try:
            copy_button_xpath = "(//button[contains(., 'Kopiuj')])[last()]"
            copy_button = WebDriverWait(config.driver, config.delay_seconds).until(
                EC.element_to_be_clickable((By.XPATH, copy_button_xpath))
            )

            config.driver.execute_script("arguments[0].click();", copy_button) # type: ignore
            time.sleep(1)

            response = clean_code(pyperclip.paste())

            if config.json:
                append_json_strings_to_array(
                    convert_paths_to_json_safe(response), config.output_file_path
                )
            else:
                mode = "w" if config.overwrite else "a"
                with open(config.output_file_path, mode, encoding="utf-8") as f:
                    f.write(response + "\n\n")

            if config.printResponse:
                print("Response:")
                print(response)
                
            return response

        except Exception as e:
            print(f"Error saving last code block: {e}")
            return None
    
    def save_response(self, output_file_path: Path=Path("response.md"), wait_time:int=60):
        try:
            last_copy_button_xpath = "(//button[contains(., 'Kopiuj') or @data-testid='copy-turn-action-button'])[last()]"
            copy_button = WebDriverWait(self.driver, wait_time).until( # type: ignore
                EC.element_to_be_clickable((By.XPATH, last_copy_button_xpath))
            )
            self.driver.execute_script("arguments[0].click();", copy_button) # type: ignore
            time.sleep(1)
            response =  clean_code(pyperclip.paste())
            with open(output_file_path, "a", encoding="utf-8") as f:
                f.write(response + "\n\n")
            return response
        except Exception as e:
            print(f"Error saving response: {e}")
            return None