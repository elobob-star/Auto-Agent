"""Single-file Harbor agent harness: --agent-import-path agent:AutoAgent."""

from __future__ import annotations

import json
import time
from datetime import datetime, timezone

from agents import Agent, Runner, function_tool
from agents.items import (
    ItemHelpers,
    MessageOutputItem,
    ReasoningItem,
    ToolCallItem,
    ToolCallOutputItem,
)
from agents.tool import FunctionTool
from agents.usage import Usage
from harbor.environments.base import BaseEnvironment
from harbor.models.agent.context import AgentContext


# ============================================================================
# EDITABLE HARNESS — prompt, tools, agent construction
# ============================================================================

SYSTEM_PROMPT = """You are a highly capable autonomous coding and terminal agent. Your goal is to solve tasks by producing the correct final artifact or system state.
You must always read /task/instruction.md first to understand what is required.
You have specialized tools for exploring the environment and reading/writing files. Use them to understand the environment and make precise edits.
Plan your steps carefully before executing them. Think about verification: how will you know your changes are correct?
Read error messages carefully and fix issues iteratively. Never give up."""
MODEL = "gpt-5"
MAX_TURNS = 30


def create_tools(environment: BaseEnvironment) -> list[FunctionTool]:
    """Create tools for the agent. Add new tools here."""

    @function_tool
    async def run_shell(command: str) -> str:
        """Run a shell command in the task environment. Returns stdout and stderr."""
        try:
            result = await environment.exec(command=command, timeout_sec=120)
            out = ""
            if result.stdout:
                out += result.stdout
            if result.stderr:
                out += f"\nSTDERR:\n{result.stderr}" if out else f"STDERR:\n{result.stderr}"
            return out or "(no output)"
        except Exception as exc:
            return f"ERROR: {exc}"

    @function_tool
    async def read_file(path: str) -> str:
        """Read the contents of a file."""
        try:
            result = await environment.exec(command=f"cat {path}", timeout_sec=30)
            return result.stdout or result.stderr or "(empty)"
        except Exception as exc:
            return f"ERROR: {exc}"

    @function_tool
    async def write_file(path: str, content: str) -> str:
        """Write content to a file, overwriting it."""
        import base64
        try:
            b64_content = base64.b64encode(content.encode()).decode()
            result = await environment.exec(command=f"echo {b64_content} | base64 -d > {path}", timeout_sec=30)
            return "File written successfully."
        except Exception as exc:
            return f"ERROR: {exc}"

    @function_tool
    async def list_directory(path: str) -> str:
        """List the contents of a directory."""
        try:
            result = await environment.exec(command=f"ls -la {path}", timeout_sec=30)
            return result.stdout or result.stderr or "(empty)"
        except Exception as exc:
            return f"ERROR: {exc}"

    @function_tool
    async def python_eval(code: str) -> str:
        '''Evaluate a python expression or script and return stdout and stderr.'''
        import base64
        try:
            b64_code = base64.b64encode(code.encode()).decode()
            result = await environment.exec(command=f'echo {b64_code} | base64 -d | python3', timeout_sec=60)
            out = ''
            if result.stdout:
                out += result.stdout
            if result.stderr:
                nl = '\n'
                out += f'{nl}STDERR:{nl}{result.stderr}' if out else f'STDERR:{nl}{result.stderr}'
            return out or '(no output)'
        except Exception as exc:
            return f'ERROR: {exc}'

    return [run_shell, read_file, write_file, list_directory, python_eval]


def create_agent(environment: BaseEnvironment) -> Agent:
    """Build the agent. Modify to add handoffs, sub-agents, or agent-as-tool."""
    tools = create_tools(environment)
    return Agent(
        name="autoagent",
        instructions=SYSTEM_PROMPT,
        tools=tools,
        model=MODEL,
    )


async def run_task(
    environment: BaseEnvironment,
    instruction: str,
) -> tuple[object, int]:
    """Run the agent on a task and return (result, duration_ms)."""
    agent = create_agent(environment)
    t0 = time.time()
    result = await Runner.run(agent, input=instruction, max_turns=MAX_TURNS)
    duration_ms = int((time.time() - t0) * 1000)
    return result, duration_ms
