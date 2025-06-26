import types
from typing import List, Optional, Type
from agents.code_task import CodeTask
from chrome_tool.agents.interface.i_chatgpt_agent import IChatGPTAgent
from chrome_tool.agents.interface.i_code_agent import ICodeAgent


class CodeAgentMock(ICodeAgent):
    def __init__(self, chatgpt_agent: IChatGPTAgent):
        self._agent = chatgpt_agent

    def execute(self, task: CodeTask) -> str | None:
        self._agent.send_prompt(task.prompt)
        return self._agent.save_code(task.output_path)

    def batch_execute(self, tasks: List[CodeTask]) -> List[Optional[str]]:
        result: List[Optional[str]] = []
        for task in tasks:
            result.append(self.execute(task))
        return result

    def open(self) -> None:
        self._agent.open()

    def close(self) -> None:
        self._agent.close()

    def __enter__(self):
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[types.TracebackType],
    ) -> None:
        self._agent.close()