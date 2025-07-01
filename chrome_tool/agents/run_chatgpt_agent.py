from pathlib import Path
from chrome_tool.agents.chatgpt_agent import ChatGPTAgent


def main():
    assumptions = "Dont use comments in code. Do not wrtie anything but code. Asume strict typing."
    function = f"Python function that calculates the Fibonacci sequence."
    test = f"Write pytest unit test for {function}. Only test, dont implement the function yet, import it from same directory."
    task = f"Write a {function} passing all tests."

    c = ChatGPTAgent()
    c.open()
    c.send_prompt(f"{assumptions} {test}")
    c.save_code(Path("data/fibonacci.test.py"))

    c.send_prompt(task)
    c.save_code(Path("data/fibonacci.py"))
    c.close()

if __name__ == "__main__":
    main()