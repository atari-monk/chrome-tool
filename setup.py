from setuptools import setup, find_packages


setup(
    name="chrome-tool",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "ai_tool=chrome_tool.run_chatgpt_agent:main",
        ],
    },
    python_requires=">=3.7",
)
