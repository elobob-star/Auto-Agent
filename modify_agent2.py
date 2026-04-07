import re

with open("agent.py", "r") as f:
    content = f.read()

# Modify SYSTEM_PROMPT
new_prompt = '''SYSTEM_PROMPT = """You are a highly capable autonomous coding and terminal agent. Your goal is to solve tasks by producing the correct final artifact or system state.
You must always read /task/instruction.md first to understand what is required.
You have specialized tools for exploring the environment and reading/writing files. Use them to understand the environment and make precise edits.
Plan your steps carefully before executing them. Think about verification: how will you know your changes are correct?
Read error messages carefully and fix issues iteratively. Never give up."""'''

content = re.sub(r'SYSTEM_PROMPT = "You are an agent that executes tasks"', new_prompt, content)

# Modify create_tools
new_tools = '''    @function_tool
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

    return [run_shell, read_file, write_file, list_directory]'''

content = re.sub(r'    return \[run_shell\]', new_tools, content)

with open("agent.py", "w") as f:
    f.write(content)
