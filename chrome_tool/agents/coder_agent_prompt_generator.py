import argparse
import json
from datetime import datetime
from pathlib import Path


def generate_config():
    default_base_path = Path("C:/atari-monk/code/utility-scripts-data")
    tasks_dir = default_base_path / "tasks"

    parser = argparse.ArgumentParser(
        description="Create or update a project tasks JSON file"
    )
    parser.add_argument(
        "--project", required=True, help="Project name (e.g., 'data_processing')"
    )
    parser.add_argument(
        "--task", required=True, help="Name of the task (e.g., 'add_numbers')"
    )
    parser.add_argument(
        "--path", default=tasks_dir, help="Base directory to save the file"
    )
    parser.add_argument("--prompt", required=True, help="Coding task prompt")
    parser.add_argument("--language", default="python", help="Programming language")

    args = parser.parse_args()

    new_task = {
        "name": args.task,
        "prompt": args.prompt,
        "output_file": f"{args.task}.py",
        "language": args.language,
        "requirements": [],
        "status": {
            "created_at": datetime.now().isoformat(),
            "completed": False,
            "last_updated": datetime.now().isoformat(),
        },
    }

    output_dir = Path(args.path)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"{args.project}.json"

    tasks = []
    if output_path.exists():
        with open(output_path, "r") as f:
            tasks = json.load(f)

    tasks.append(new_task)

    with open(output_path, "w") as f:
        json.dump(tasks, f, indent=2)

    print(f"Task added to project at: {output_path}")

def main():
    generate_config()

if __name__ == "__main__":
    main()
