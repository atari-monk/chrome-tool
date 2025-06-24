# Code Agent

High-Level Agent for code generation

## Usage Examples

### Single Task

```python
agent = CodeAgent()
task = CodeTask(
    prompt="Python async websocket client",
    output_path=Path("websocket_client.py")
)
agent.execute(task)
```

### Batch Processing

```python
tasks = [
    CodeTask(prompt="FastAPI endpoint", output_path=Path("api.py")),
    CodeTask(prompt="Pydantic model", output_path=Path("models.py"))
]

with CodeAgent() as agent:
    agent.batch_execute(tasks)
```

### Persistent Session

```python
agent = CodeAgent(persist_session=True)
# Multiple independent operations...
agent.execute(task1)
agent.execute(task2)
agent._agent.close()
```