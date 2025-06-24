import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from valid_url import is_valid_url
from chatgpt.config.chatgpt_config import ChatGPTConfig
from chrome_profiles import get_chrome_profile


def open_chrome_with_profile(config: ChatGPTConfig) -> webdriver.Chrome | None:
    if not is_valid_url(config.page):
        raise ValueError(f"Invalid URL: '{config.page}'. Must include scheme (e.g., https://) and domain.")
    
    if not (profile := get_chrome_profile(config.config_path)):
        print("No active Chrome profile found")
        return None
    
    active_profile = profile["chromeProfilePath"]
    profile_directory = profile["profileDirectory"]
    custom_path = profile["customPath"]
    if custom_path:
        active_profile = custom_path
    print(f"Active Profile: {active_profile}, Profile Directory: {profile_directory}")

    options = Options()
    options.add_argument(rf"user-data-dir={active_profile}") # type: ignore
    options.add_argument(f"profile-directory={profile_directory}") # type: ignore
    options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"]) # type: ignore
    options.add_argument("--disable-blink-features=AutomationControlled") # type: ignore
    options.add_argument("--log-level=3") # type: ignore
    options.add_argument("--disable-gpu") # type: ignore
    options.add_argument("--disable-dev-shm-usage") # type: ignore
    options.add_argument("--no-sandbox") # type: ignore
    
    if config.detach:
        options.add_experimental_option("detach", True) # type: ignore

    service = Service()
    service.creationflags = 0x08000000  # type: ignore
    service.quiet = True # type: ignore

    os.environ['WDM_LOG_LEVEL'] = '0'
    os.environ['WDM_PRINT_FIRST_LINE'] = 'False'

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(config.page)
    print(f"Successfully opened: {config.page}")
    return driver