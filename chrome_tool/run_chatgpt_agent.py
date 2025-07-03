from pathlib import Path
from chrome_tool.chatgpt_agent import ChatGPTAgent


def main():
    prompt_1 = """
    Rules :
    - Strict types
    - Dont use any type of comments in code
    - Write only ONE code block, no other text
    Task : I want to implement Fibonacci sequence function in TDD style, so first write pytest unit tests for it.
    'from chrome_tool.tmp.fibonacci import fibonacci' use this import.
    """

    prompt_2 = """
    Task : Write python function that calculates the Fibonacci sequence. 
    Pass all tests."""

    c = ChatGPTAgent()
    c.open()
    c.send_prompt(prompt_1)
    c.save_code(Path("test_fibonacci.py"))

    c.send_prompt(prompt_2)
    c.save_code(Path("fibonacci.py"))
    c.close()

if __name__ == "__main__":
    main()