import json
import os
from pathlib import Path
from typing import Union


def get_chrome_profile(config_file_path: Union[Path, str]) -> dict[str, str] | None:
    if config_file_path is str:
        config_file_path = Path(config_file_path)
    if config_file_path is Path and not config_file_path.exists():
        print(f"Config file does not exist: {config_file_path}")
        return None
    try:
        with open(config_file_path) as f:
            config = json.load(f)

        for computer in config["computers"]:
            profile_path = config["chromeProfilePath"].replace(
                "{userName}", computer["userName"]
            )
            if os.path.exists(profile_path):
                return {
                    "computerName": computer["computerName"],
                    "userName": computer["userName"],
                    "chromeProfilePath": profile_path,
                    "profileDirectory": computer["profileDirectory"],
                    "customPath": computer["customPath"]
                }
        return None

    except Exception as e:
        print(f"Error loading active profile: {str(e)}")
        return None


def main():
    if profile := get_chrome_profile(r"C:\atari-monk\code\apps-data-store\chrome_profiles.json"):
        print(f"Active Profile: {profile['chromeProfilePath']}")
    else:
        print("No active Chrome profile found")


if __name__ == "__main__":
    main()
