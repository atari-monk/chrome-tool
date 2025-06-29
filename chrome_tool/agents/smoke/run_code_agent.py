from pathlib import Path
from chrome_tool.agents.chatgpt_agent import ChatGPTAgent
from chrome_tool.agents.code_agent import CodeAgent
from chrome_tool.agents.code_task import CodeTask


def code_agent_smoke_test():
    task = CodeTask(
        prompt="print('Hello from smoke test!')",
        delay_seconds=0,
        output_path=Path("output.py"),
        json_output=False,
    )

    agent = CodeAgent(ChatGPTAgent())
    try:
        agent.open()
        agent.execute(task)
        print("execute() without persistence passed")
    except Exception as e:
        print(f"execute() without persistence failed: {e}")

    agent = CodeAgent(ChatGPTAgent())
    try:
        agent.open()
        agent.batch_execute([task, task])
        print("batch_execute() with persistence passed")
    except Exception as e:
        print(f"batch_execute() with persistence failed: {e}")
    finally:
        agent.__exit__(None, None, None)
        
    try:
        with CodeAgent(ChatGPTAgent()) as agent:
            agent.open()
            agent.execute(task)
        print("context manager usage passed")
    except Exception as e:
        print(f"context manager usage failed: {e}")

if __name__ == "__main__":
    code_agent_smoke_test()