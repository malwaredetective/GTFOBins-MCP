import os
import json
from fastmcp import FastMCP
from typing import Annotated
import logging

logging.basicConfig(level=logging.INFO)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
API_JSON_PATH = os.path.join(SCRIPT_DIR, "api.json")
FUNCTIONS_JSON_PATH = os.path.join(SCRIPT_DIR, "functions.json")
MCP_SERVER_NAME = "gtfobins-mcp-server"

mcp = FastMCP(MCP_SERVER_NAME)

def load_json(path):
    """Helper function to load a JSON file."""
    if not os.path.exists(path):
        logging.error(f"File not found: {path}")
        return {"Error": f"{path} does not exist. Please ensure the file is in the correct location."}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def format_code_blocks(data):
    """Helper function to format any code block fields in a consistent way."""
    if isinstance(data, dict):
        for key, value in data.items():
            if key == "code" and isinstance(value, str):
                data[key] = f"```bash\n{value}\n```"
            elif isinstance(value, (dict, list)):
                format_code_blocks(value)
    elif isinstance(data, list):
        for item in data:
            format_code_blocks(item)
    return data

@mcp.tool(description="Return a list of all unix binaries found within GTFOBins.")
def list_binaries():
    """List all binaries from api.json."""
    try:
        api_data = load_json(API_JSON_PATH)
        return sorted(list(api_data.keys()))
    except Exception as e:
        return {"Error": f"Could not retrieve binaries: {str(e)}!"}
    
@mcp.tool(description="List all binaries that have a specific function. For example, list all binaries with 'suid' functionality.")
def list_binaries_by_function(function_name: Annotated[str, "The function name to filter binaries by, for example: 'suid', 'file-read'."]):
    """List all binaries that include a given function."""
    try:
        api_data = load_json(API_JSON_PATH)
        matching_binaries = {}

        for binary, details in api_data.items():
            if function_name in details.get("functions", {}):
                matching_binaries[binary] = format_code_blocks(details["functions"][function_name])

        if matching_binaries:
            return matching_binaries
        else:
            return {"Error": f"No binaries found with the function '{function_name}'."}
    except Exception as e:
        return {"Error": f"Could not retrieve binaries by function: {str(e)}"}

@mcp.tool(description="Return a list of all functions and their descriptions from GTFOBins.")
def list_functions():
    """List all functions and their descriptions from functions.json."""
    try:
        functions_data = load_json(FUNCTIONS_JSON_PATH)
        return functions_data.get("functions", {})
    except Exception as e:
        return {"Error": f"Could not retrieve functions: {str(e)}"}

@mcp.tool(description="Fetch all the details of a specific unix binary from GTFOBins by name.")
def query_binary(binary_name: Annotated[str, "The name of the binary to query, for example: 'base64' or 'find'."]):
    """Query a specific binary by name in api.json."""
    try:
        api_data = load_json(API_JSON_PATH)
        binary = api_data.get(binary_name)
        if binary:
            return format_code_blocks(binary)
        else:
            return {"Error": f"Binary '{binary_name}' not found in api.json."}
    except Exception as e:
        return {"Error": f"Could not query binary: {str(e)}"}

@mcp.tool(description="Fetch the description for a specific function from GTFOBins by name.")
def query_function(function_name: Annotated[str, "The function name to query, for example:'file-read', 'suid'."]):
    """Query a specific function by name in functions.json."""
    try:
        functions_data = load_json(FUNCTIONS_JSON_PATH)
        functions = functions_data.get("functions", {})
        function = functions.get(function_name)
        if function:
            return function
        else:
            return {"Error": f"Function '{function_name}' not found in functions.json."}
    except Exception as e:
        return {"Error": f"Could not query function: {str(e)}"}

if __name__ == "__main__":
    logging.info(f"Starting MCP server: {MCP_SERVER_NAME}")
    mcp.run()