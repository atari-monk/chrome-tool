from pathlib import Path
from chrome_tool.agent import Agent


def main():
    prompt_1 = """
Create comprehensive pytest unit tests for a Fibonacci sequence function following strict TDD principles. Requirements:
1. Test all edge cases including 0, 1, and invalid inputs
2. Include type checking tests
3. Test the first 10 Fibonacci numbers
4. Use this exact import: 'from chrome_tool.fibonacci import fibonacci'
5. Follow these strict rules:
   - No comments in code
   - Strong type checking
   - Only include the test code block with no additional text
   - All tests must fail when the implementation doesn't exist
    """

    prompt_2 = """
Implement a Fibonacci sequence function that passes all tests with these requirements:
1. Must match this signature: `def fibonacci(n: int) -> int:`
2. Handle invalid inputs with ValueError
3. Optimize for O(n) time complexity
4. Follow these strict rules:
   - No comments in code
   - Strong type hints
   - Only include the implementation code block
   - Must pass all tests from the test phase
5. Implementation must be iterative (not recursive)
    """

    c = Agent()
    c.open_chrome_with_profile()
    c.send_prompt(prompt_1)
    c.save_code(Path("generated/test_fibonacci.py"))

    c.send_prompt(prompt_2)
    c.save_code(Path("generated/fibonacci.py"))
    c.close()

if __name__ == "__main__":
    main()