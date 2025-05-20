# tool_dispatcher.py
'''
Provides a dynamic tool execution mechanism.

This module allows for calling functions (tools) based on a string name.
Tools are registered in the `TOOL_REGISTRY` dictionary, which maps tool
names (strings) to their corresponding callable functions.

To add a new tool:
1. Import the tool function.
2. Add an entry to `TOOL_REGISTRY` with the desired tool name as the key
   and the function object as the value.

Main component:
- `execute_tool(tool_name: str, tool_args: dict)`: Executes a registered tool.
'''
from arxiv_searcher import search_papers, extract_info # Assuming arxiv_searcher.py is in the same directory or PYTHONPATH

class ToolNotFoundError(Exception):
    '''Raised when a tool name is not found in the TOOL_REGISTRY.'''
    pass

TOOL_REGISTRY = {
    "search_papers": search_papers,
    "extract_info": extract_info,
}

def execute_tool(tool_name: str, tool_args: dict):
    '''
    Executes a tool identified by tool_name with specified arguments.

    Args:
        tool_name: The string name of the tool to execute.
        tool_args: A dictionary of arguments to pass to the tool function.

    Returns:
        The result of the called tool function.

    Raises:
        ToolNotFoundError: If the tool_name is not found in TOOL_REGISTRY.
    '''
    if tool_name in TOOL_REGISTRY:
        tool_function = TOOL_REGISTRY[tool_name]
        return tool_function(**tool_args)
    else:
        raise ToolNotFoundError(f"Tool '{tool_name}' not found.")
