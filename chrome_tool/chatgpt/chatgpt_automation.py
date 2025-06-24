from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyperclip
import time
from chatgpt.config.code_block_config import CodeBlockConfig
from chatgpt.config.prompt_config import PromptConfig
from json_utils import (
    append_json_strings_to_array,
    convert_paths_to_json_safe,
)
from string_utils import clean_code
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


def send_prompt(config: PromptConfig) -> bool:
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


def save_response(driver: webdriver.Chrome, output_file_path: Path=Path("response.md"), wait_time:int=60):
    try:
        last_copy_button_xpath = "(//button[contains(., 'Kopiuj') or @data-testid='copy-turn-action-button'])[last()]"
        copy_button = WebDriverWait(driver, wait_time).until(
            EC.element_to_be_clickable((By.XPATH, last_copy_button_xpath))
        )
        driver.execute_script("arguments[0].click();", copy_button) # type: ignore
        time.sleep(1)
        response =  clean_code(pyperclip.paste())
        with open(output_file_path, "a", encoding="utf-8") as f:
            f.write(response + "\n\n")
        return response
    except Exception as e:
        print(f"Error saving response: {e}")
        return None


def save_code_block(config: CodeBlockConfig):
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

        return response

    except Exception as e:
        print(f"Error saving last code block: {e}")
        return None
