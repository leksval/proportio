# MCP Client Configuration Examples

This document provides configuration examples for various MCP clients to connect to the Proportio server.

## Cursor IDE

### Method 1: Settings JSON

Add to your Cursor settings (`Cmd/Ctrl + ,` → Open Settings JSON):

```json
{
  "mcpServers": {
    "proportio": {
      "url": "http://localhost:7860/gradio_api/mcp/sse",
      "headers": {
        "X-Api-Key": "your-secure-token-here"
      }
    }
  }
}
```

### Method 2: Workspace Configuration

Create `.cursor/mcp.json` in your project root:

```json
{
  "proportio": {
    "url": "http://localhost:7860/gradio_api/mcp/sse",
    "headers": {
      "X-Api-Key": "your-secure-token-here"
    }
  }
}
```

## Claude Desktop

### Configuration File Location

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

### Local Server Configuration

```json
{
  "mcpServers": {
    "proportio": {
      "command": "python",
      "args": ["/path/to/proportio/app.py"],
      "env": {
        "MCP_TOKEN": "your-secure-token-here"
      }
    }
  }
}
```

### Remote Server Configuration

```json
{
  "mcpServers": {
    "proportio": {
      "url": "https://your-server.com/gradio_api/mcp/sse",
      "headers": {
        "X-Api-Key": "your-secure-token-here"
      }
    }
  }
}
```

## CrewAI

### Basic Setup

```python
from crewai import Agent, Task, Crew
from crewai.tools import MCPTool

# Configure the MCP tool
proportio_tool = MCPTool(
    name="proportio_calculator",
    url="http://localhost:7860/gradio_api/mcp/sse",
    headers={"X-Api-Key": "your-secure-token-here"}
)

# Create an agent with the tool
math_agent = Agent(
    role="Mathematical Calculator",
    goal="Perform accurate proportion and percentage calculations",
    backstory="You are an expert mathematician who uses reliable tools for calculations.",
    tools=[proportio_tool],
    verbose=True
)

# Example task
calculation_task = Task(
    description="Calculate what percentage 75 is of 300, then scale that result by 1.5",
    agent=math_agent,
    expected_output="The percentage and scaled result with explanations"
)

# Run the crew
crew = Crew(
    agents=[math_agent],
    tasks=[calculation_task]
)

result = crew.kickoff()
print(result)
```

### Advanced CrewAI Setup with Multiple Tools

```python
from crewai import Agent, Task, Crew
from crewai.tools import MCPTool

class ProportioTools:
    def __init__(self, base_url="http://localhost:7860", api_key="your-token"):
        self.base_url = f"{base_url}/gradio_api/mcp/sse"
        self.headers = {"X-Api-Key": api_key}
    
    def get_tools(self):
        return [
            MCPTool(
                name="percent_calculator",
                url=self.base_url,
                headers=self.headers,
                description="Calculate percentages accurately"
            ),
            MCPTool(
                name="proportion_solver",
                url=self.base_url,
                headers=self.headers,
                description="Solve proportion equations"
            ),
            MCPTool(
                name="dimension_resizer",
                url=self.base_url,
                headers=self.headers,
                description="Resize dimensions with scaling"
            )
        ]

# Usage
proportio = ProportioTools(api_key="your-secure-token-here")
tools = proportio.get_tools()

agent = Agent(
    role="Design Calculator",
    goal="Help with design calculations and proportions",
    tools=tools
)
```

## OpenAI Agents SDK

### Basic Configuration

```python
from openai_agents import Agent
from openai_agents.mcp import MCPConnection

# Setup MCP connection
mcp_conn = MCPConnection(
    url="http://localhost:7860/gradio_api/mcp/sse",
    headers={"X-Api-Key": "your-secure-token-here"}
)

# Create agent with MCP tools
agent = Agent(
    name="Math Assistant",
    model="gpt-4",
    mcp_connections=[mcp_conn]
)

# Use the agent
response = agent.run("What percentage is 45 out of 180?")
print(response)
```

## Generic HTTP Client (for testing)

### Using curl

```bash
# Test percent_of tool
curl -X POST http://localhost:7860/gradio_api/mcp/sse \
  -H "X-Api-Key: your-secure-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "percent_of",
      "arguments": {
        "part": 25,
        "whole": 100
      }
    }
  }'
```

### Using Python requests

```python
import requests
import json

def call_proportio_tool(tool_name, arguments, api_key="your-token"):
    url = "http://localhost:7860/gradio_api/mcp/sse"
    headers = {
        "X-Api-Key": api_key,
        "Content-Type": "application/json"
    }
    
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments
        }
    }
    
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

# Examples
result1 = call_proportio_tool("percent_of", {"part": 75, "whole": 300})
print(f"Percentage: {result1}")

result2 = call_proportio_tool("solve_proportion", {"a": 3, "b": 4, "c": 6, "d": None})
print(f"Missing value: {result2}")

result3 = call_proportio_tool("resize_dimensions", {
    "width": 1920, 
    "height": 1080, 
    "scale": 0.5
})
print(f"New dimensions: {result3}")
```

## Environment-Specific Configurations

### Development Environment

```bash
# .env file
MCP_TOKEN=dev-token-123
DEBUG=true
LOG_LEVEL=DEBUG
RELOAD=true
```

### Production Environment

```bash
# .env file
MCP_TOKEN=prod-secure-token-xyz789
DEBUG=false
LOG_LEVEL=WARNING
MAX_REQUEST_SIZE=32768
```

### Hugging Face Spaces

Set these as Space secrets:

- `MCP_TOKEN`: Your secure authentication token
- `LOG_LEVEL`: `INFO` or `WARNING`

Access URL: `https://your-username-proportio.hf.space/gradio_api/mcp/sse`

## Security Best Practices

### Token Generation

Generate secure tokens:

```bash
# Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# OpenSSL
openssl rand -base64 32

# Node.js
node -e "console.log(require('crypto').randomBytes(32).toString('base64url'))"
```

### Token Rotation

1. Generate new token
2. Update all client configurations
3. Update server environment variable
4. Restart server
5. Verify all clients work with new token

### Network Security

- Use HTTPS in production
- Implement rate limiting at reverse proxy level
- Monitor for unusual usage patterns
- Keep logs for security auditing

## Troubleshooting

### Common Connection Issues

1. **"Connection refused"**
   - Check if server is running: `curl http://localhost:7860`
   - Verify port is not blocked by firewall

2. **"Invalid API key"**
   - Ensure `X-Api-Key` header is included
   - Check token matches `MCP_TOKEN` environment variable
   - Verify no extra spaces or characters in token

3. **"Request timeout"**
   - Check server logs for errors
   - Verify network connectivity
   - Increase client timeout settings

### Debug Mode

Enable debug logging to troubleshoot issues:

```bash
export DEBUG=true
export LOG_LEVEL=DEBUG
python app.py
```

This will show detailed logs of all MCP requests and responses.

## Roo Code Assistant

### Configuration

Roo uses MCP servers automatically when they're running locally. Simply start the Proportio server:

```bash
python app.py
```

Roo will detect the running MCP server at `http://localhost:7860/gradio_api/mcp/sse` and make the tools available.

### Usage Examples

```
Human: Calculate what percentage 45 is of 180

Roo: I'll use the proportion calculator to find what percentage 45 is of 180.

[Using percent_of tool with part=45, whole=180]

45 is 25% of 180.
```

```
Human: I need to resize an image from 1920x1080 to half the size

Roo: I'll help you calculate the new dimensions using the resize tool.

[Using resize_dimensions tool with width=1920, height=1080, scale=0.5]

The new dimensions would be 960 × 540 pixels.
```

## OpenWebUI

### Configuration File

Add to your OpenWebUI configuration (`config.yaml` or environment):

```yaml
mcp:
  servers:
    proportio:
      url: "http://localhost:7860/gradio_api/mcp/sse"
      headers:
        X-Api-Key: "your-secure-token-here"
      tools:
        - percent_of
        - solve_proportion
        - scale_by_ratio
        - direct_k
        - resize_dimensions
```

### Environment Variables

```bash
# OpenWebUI MCP configuration
OPENWEBUI_MCP_SERVERS='[
  {
    "name": "proportio",
    "url": "http://localhost:7860/gradio_api/mcp/sse",
    "headers": {"X-Api-Key": "your-secure-token-here"}
  }
]'
```

### Docker Compose with OpenWebUI

```yaml
version: '3.8'
services:
  proportio:
    build: .
    ports:
      - "7860:7860"
    environment:
      - MCP_TOKEN=your-secure-token-here
    networks:
      - webui_network

  openwebui:
    image: ghcr.io/open-webui/open-webui:main
    ports:
      - "3000:8080"
    environment:
      - OPENWEBUI_MCP_SERVERS=[{"name":"proportio","url":"http://proportio:7860/gradio_api/mcp/sse","headers":{"X-Api-Key":"your-secure-token-here"}}]
    depends_on:
      - proportio
    networks:
      - webui_network

networks:
  webui_network:
    driver: bridge
```

## Msty

### Configuration

In Msty's settings, add the MCP server:

```json
{
  "mcp_servers": {
    "proportio": {
      "type": "sse",
      "url": "http://localhost:7860/gradio_api/mcp/sse",
      "auth": {
        "type": "header",
        "header_name": "X-Api-Key",
        "header_value": "your-secure-token-here"
      },
      "description": "Mathematical proportion calculations"
    }
  }
}
```

### Using with Msty

1. Start the Proportio server: `python app.py`
2. Open Msty and go to Settings → MCP Servers
3. Add a new server with the configuration above
4. The tools will be available in chat sessions

### Example Msty Usage

```
You: I need to solve this proportion: 3/4 = x/12. What is x?

Msty: I'll use the proportion solver to find the missing value.

[Using solve_proportion tool]

The missing value x is 9. So 3/4 = 9/12.
```

## Local Development Setup Script

Create a setup script for easy local development:

```bash
#!/bin/bash
# setup_local_mcp.sh

# Generate secure token
TOKEN=$(python -c "import secrets; print(secrets.token_urlsafe(32))")

# Create .env file
cat > .env << EOF
MCP_TOKEN=$TOKEN
DEBUG=true
LOG_LEVEL=DEBUG
RELOAD=true
EOF

echo "Generated secure token: $TOKEN"
echo "Add this to your MCP clients' X-Api-Key header"

# Start the server
python app.py
```

Make it executable: `chmod +x setup_local_mcp.sh`

## Testing Your MCP Connection

### Quick Test Script

```python
#!/usr/bin/env python3
"""Test script for Proportio MCP server connection"""

import requests
import json
import sys

def test_mcp_connection(base_url="http://localhost:7860", api_key="your-token"):
    """Test MCP server connection and tools."""
    
    url = f"{base_url}/gradio_api/mcp/sse"
    headers = {
        "X-Api-Key": api_key,
        "Content-Type": "application/json"
    }
    
    # Test cases
    tests = [
        {
            "name": "Percentage Calculation",
            "tool": "percent_of",
            "args": {"part": 25, "whole": 100},
            "expected": 25.0
        },
        {
            "name": "Proportion Solving",
            "tool": "solve_proportion", 
            "args": {"a": 3, "b": 4, "c": 6, "d": None},
            "expected": 8.0
        },
        {
            "name": "Dimension Resizing",
            "tool": "resize_dimensions",
            "args": {"width": 100, "height": 50, "scale": 2.0},
            "expected": {"new_width": 200.0, "new_height": 100.0}
        }
    ]
    
    print(f"Testing MCP server at {url}")
    print(f"Using API key: {api_key[:8]}...")
    print("-" * 50)
    
    for test in tests:
        try:
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": test["tool"],
                    "arguments": test["args"]
                }
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ {test['name']}: PASSED")
                print(f"   Result: {result}")
            else:
                print(f"❌ {test['name']}: FAILED (HTTP {response.status_code})")
                print(f"   Response: {response.text}")
                
        except Exception as e:
            print(f"❌ {test['name']}: ERROR - {str(e)}")
        
        print()

if __name__ == "__main__":
    api_key = input("Enter your API key (or press Enter for 'test-token'): ").strip()
    if not api_key:
        api_key = "test-token"
    
    test_mcp_connection(api_key=api_key)
```

Save as `test_mcp.py` and run: `python test_mcp.py`

This comprehensive guide covers all major MCP clients including Roo, OpenWebUI, and Msty, providing practical examples for integrating the Proportio server into your development workflow.