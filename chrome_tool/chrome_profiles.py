from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class ChromeProfile:
    path: Path
    name: str

def get_first_chrome_profile() -> Optional[ChromeProfile]:
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

def main():
    if profile := get_first_chrome_profile():
        print(f"Found Chrome profile: {profile.path} ({profile.name})")
    else:
        print("No Chrome profiles found")

if __name__ == "__main__":
    main()