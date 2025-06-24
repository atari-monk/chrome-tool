import argparse
from pathlib import Path
import pyperclip


def get_class_code(path: Path):
    with open(path, "r") as f:
        return f.read()


def generate_template(class_code: str, path: Path) -> str:
    return f"""Given a class:

<class code>
{class_code}
</class code>

Return a minimal but comprehensive JSON representation optimized for:
1. Quick understanding of the class's purpose
2. Clear state/dependencies tracking
3. Easy comparison across classes
4. Return only json!

{{
  "class": "<name>",                         // Canonical name (use exact class name)
  "path": "{path}",                  // Full path
  "type": "",  // Semantic category (choose: utility/entity/service/controller/model/view/other)
  "purpose": "",         // 1-sentence active-voice description (e.g., "Manages user authentication")
  "state": [],     // List critical instance/class attributes that represent object state
  "interface": [],   // List public methods that form the API/contract
  "deps": {{
    "internal": [],    // Other classes from this codebase it directly uses
    "external": []              // Third-party modules/packages it imports
  }},
  "metrics": {{                               // (Fill these if available)
    "complexity": 0,                     // Cyclomatic complexity score
    "loc": 0                   // Lines of code (excluding comments/whitespace)
  }}
}}"""


def copy_to_clipboard(template: str):
    pyperclip.copy(template)
    print("Template with AI guidance comments copied to clipboard!")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Path to Python file containing the class")
    args = parser.parse_args()
    class_code = get_class_code(args.path)
    template = generate_template(class_code, args.path)
    copy_to_clipboard(template)


if __name__ == "__main__":
    main()
