import subprocess
import psutil
from pathlib import Path
from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyperclip
import time
from chrome_tool.prompt_config import PromptConfig
from chrome_tool.code_block_config import CodeBlockConfig
from chrome_tool.utils.string import clean_code
from chrome_tool.utils.json import append_json_strings_to_array, convert_paths_to_json_safe
from chrome_tool.utils.url import is_valid_url
from chrome_tool.chrome_profile import ChromeProfile
from chrome_tool.agent_config import AgentConfig
from chrome_tool.utils.colorama import color_print
from colorama import Fore, Style


class Agent:
    def __init__(self):
        self.driver = None

    def ensure_chrome_running(self, profile: ChromeProfile, port: int = 9222):
        # ✅ Check if Chrome with --remote-debugging is already running
        for proc in psutil.process_iter(['name', 'cmdline']): # type: ignore
            if (
                proc.info['name']
                and 'chrome' in proc.info['name'].lower()
                and '--remote-debugging-port={}'.format(port) in ' '.join(proc.info['cmdline'])
            ):
                return  # Already running

        # ✅ Start Chrome with remote debugging
        print(f"Starting Chrome with remote debugging on port {port}...")
        chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        subprocess.Popen([
            chrome_path,
            f"--remote-debugging-port={port}",
            f"--user-data-dir={profile.path}",
            f"--profile-directory={profile.name}"
        ])

        # ✅ Give Chrome a moment to fully start
        time.sleep(2)

    def open_chrome_with_profile(self, config: AgentConfig = AgentConfig(
        page="https://chat.openai.com/"
    )) -> None:
        color_print("Connecting to existing Chrome...\n", Fore.RED, style=Style.BRIGHT)

        if not is_valid_url(config.page):
            raise ValueError(f"Invalid URL: '{config.page}'")

        profile = self._get_first_chrome_profile()
        if not profile:
            raise RuntimeError("No valid Chrome profile found!")

        self.ensure_chrome_running(profile)

        # ✅ Attach to running Chrome
        options = Options()
        options.debugger_address = "127.0.0.1:9222"

        try:
            self.driver = webdriver.Chrome(options=options)
            self.driver.get(config.page)
            print(f"Connected and opened: {config.page}")
        except Exception as e:
            print(f"Could not attach to Chrome: {e}")

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
        if self.driver:
            try:
                self.driver.quit()
            except Exception as e:
                print(f"Error while closing driver: {e}")
            finally:
                self.driver = None

    def send_prompt(self, prompt: str, config: PromptConfig = PromptConfig()) -> bool:
        if self.driver is None:
            raise Exception("ChatGPT session is not open.")
        color_print("Press Enter to send prompt...\n", Fore.RED, style=Style.BRIGHT)
        input()
        if config.printPrompt:
            print(prompt)
        try:
            pyperclip.copy(prompt)
            input_area = self.driver.find_element(By.ID, config.input_area_id)
            input_area.clear()
            input_area.click()

            if self.driver.name in ['chrome', 'edge']:
                input_area.send_keys(Keys.CONTROL, 'v')
            elif self.driver.name == 'firefox':
                input_area.send_keys(Keys.COMMAND, 'v')

            input_area.send_keys(Keys.RETURN)
            print("Prompt sent successfully.")
            return True
        except Exception as e:
            print(f"Failed to send prompt: {e}")
            return False

    def save_code(self, output_file_path: Path) -> Optional[str]:
        if self.driver is None:
            raise Exception("ChatGPT session is not open.")
        color_print("Saving Response...\n", Fore.RED, style=Style.BRIGHT)
        config = CodeBlockConfig(driver=self.driver, output_file_path=output_file_path, overwrite=True)
        input("Press Enter to save...")
        try:
            copy_button_xpath = "(//button[contains(., 'Kopiuj')])[last()]"
            copy_button = WebDriverWait(self.driver, config.delay_seconds).until(
                EC.element_to_be_clickable((By.XPATH, copy_button_xpath))
            )
            self.driver.execute_script("arguments[0].click();", copy_button) # type: ignore
            time.sleep(1)
            response = clean_code(pyperclip.paste())

            if config.json:
                append_json_strings_to_array(convert_paths_to_json_safe(response), config.output_file_path)
            else:
                mode = "w" if config.overwrite else "a"
                with open(config.output_file_path, mode, encoding="utf-8") as f:
                    f.write(response + "\n\n")

            if config.printResponse:
                print("Response:")
                print(response)

            return response
        except Exception as e:
            print(f"Error saving code: {e}")
            return None

    def save_response(self, output_file_path: Path = Path("response.md"), wait_time: int = 60) -> Optional[str]:
        if self.driver is None:
            raise Exception("ChatGPT session is not open.")
        try:
            last_copy_button_xpath = "(//button[contains(., 'Kopiuj') or @data-testid='copy-turn-action-button'])[last()]"
            copy_button = WebDriverWait(self.driver, wait_time).until(
                EC.element_to_be_clickable((By.XPATH, last_copy_button_xpath))
            )
            self.driver.execute_script("arguments[0].click();", copy_button) # type: ignore
            time.sleep(1)
            response = clean_code(pyperclip.paste())
            with open(output_file_path, "a", encoding="utf-8") as f:
                f.write(response + "\n\n")
            return response
        except Exception as e:
            print(f"Error saving response: {e}")
            return None
