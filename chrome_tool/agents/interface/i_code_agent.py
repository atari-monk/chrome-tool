from agents.code_task import CodeTask
import types
from typing import List, Optional, Protocol, Type, runtime_checkable


@runtime_checkable
class ICodeAgent(Protocol):
    def execute(self, task: CodeTask) -> Optional[str]: ...

    def batch_execute(self, tasks: List[CodeTask]) -> List[Optional[str]]: ...

    def open(self) -> None: ...

    def close(self) -> None: ...

    def __enter__(self) -> "ICodeAgent": ...

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[types.TracebackType],
    ) -> None: ...