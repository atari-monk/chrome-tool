from pathlib import Path
import argparse
from chrome_tool.agents.chatgpt_agent import ChatGPTAgent
from chrome_tool.agents.generate_class_template import (
    generate_template,
    get_class_code,
)
from chrome_tool.files import get_py_files

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Path to Python file containing the class")
    args = parser.parse_args()

    base_path = Path(r"C:\atari-monk\code\apps-data-store\code_base")
    input_path = Path(args.path)

    if input_path.is_dir():
        py_files = get_py_files(input_path)
        output_path = base_path / f"{input_path.stem}.json"
    else:
        py_files = [input_path]
        output_path = base_path / f"{input_path.stem}.json"

    c = ChatGPTAgent()
    for file_path in py_files:
        class_code = get_class_code(file_path)
        prompt = generate_template(class_code, file_path)
        c.send_prompt(prompt)
        c.save_code(output_path)
    c.close()

if __name__ == "__main__":
    main()
