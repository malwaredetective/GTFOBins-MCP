# GTFOBins-MCP
![python](https://img.shields.io/badge/python-3.11%2B-blue)
![MCP Server](https://img.shields.io/badge/MCP-Server-blueviolet)
![License: MIT](https://img.shields.io/badge/license-MIT-green)

A Model Context Protocol (MCP) server that acts as a bridge between Large Language Models (LLMs) and a local [GTFOBins](https://gtfobins.github.io/) API, allowing automated queries for Unix binaries that can be used to bypass local security restrictions in misconfigured systems.

> This MCP Server is configured to run locally via STDIO.

## Quickstart Guide

### 1. Clone the Repository

```bash
git clone https://github.com/malwaredetective/GTFOBins-MCP.git
cd GTFOBins-MCP
```

### 2. Set Up a Python Virtual Environment

```bash
python3 -m venv venv

# Run this command to activate your Python Virtual Environment within Linux/macOS
source venv/bin/activate

# Run this command to activate your Python Virtual Environment within Windows
venv\Scripts\activate
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the MCP Server within your preferred MCP Client

- Install your preferred MCP Client.
- Depending on your MCP Client, the steps to configure the [GTFOBins-MCP](gtfobins-mcp-server.py) server may differ. A standard configuration is listed within this projects [mcp.json](mcp.json) file.

> Note: When executing the MCP server from within a Python Virtual Environment, the startup command may differ depending on your Operating System.

### list_binaries
Return a list of all unix binaries found within GTFOBins.

```json
{
  "type": "object",
  "properties": {}
}
```

### list_binaries_by_function
List all binaries that have a specific function. For example, list all binaries with 'suid' functionality.

```json
{
  "type": "object",
  "properties": {
    "function_name": {
      "description": "The function name to filter binaries by, e.g., 'suid', 'file-read'.",
      "type": "string"
    }
  },
  "required": [
    "function_name"
  ]
}
```

### list_functions
Return a list of all functions and their descriptions from GTFOBins.

```json
{
  "type": "object",
  "properties": {}
}
```

### query_binary
Fetch all the details of a specific unix binary from GTFOBins by name.

```json
{
  "type": "object",
  "properties": {
    "binary_name": {
      "description": "The name of the binary to query, for example: 'base64' or 'find'.",
      "type": "string"
    }
  },
  "required": [
    "binary_name"
  ]
}
```

### query_function
Fetch the description for a specific function from GTFOBins by name.

```json
{
  "type": "object",
  "properties": {
    "function_name": {
      "description": "The function name to query, for example: 'file-read', 'suid'.",
      "type": "string"
    }
  },
  "required": [
    "function_name"
  ]
}
```

## License

This project is licensed under the [MIT License](LICENSE).

You are free to use, modify, and distribute this software in accordance with the MIT License terms.