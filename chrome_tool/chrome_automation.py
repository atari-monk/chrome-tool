import os
from typing import Optional, Any, cast
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeWebDriver
from chrome_tool.chrome_profiles import get_first_chrome_profile
from chrome_tool.utils.url import is_valid_url
from chrome_tool.chatgpt_config import ChatGPTConfig
from colorama import Fore, Style
from chrome_tool.utils.colorama import color_print


def open_chrome_with_profile(config: ChatGPTConfig) -> Optional[ChromeWebDriver]:
    color_print(f"Initializing Chrome with profile...\n", Fore.RED, style=Style.BRIGHT)
    if not is_valid_url(config.page):
        raise ValueError(f"Invalid URL: '{config.page}'. Must include scheme (e.g., https://) and domain.")
    
    if not (profile := get_first_chrome_profile()):
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

        driver = webdriver.Chrome(service=service, options=options)
        driver.get(config.page)
        print(f"Successfully opened: {config.page}")
        return driver
    except Exception as e:
        print(f"Failed to start Chrome: {str(e)}")
        return None