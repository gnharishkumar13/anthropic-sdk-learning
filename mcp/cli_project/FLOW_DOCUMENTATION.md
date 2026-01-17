# MCP Chat - Program Flow Documentation

## Program Startup and Flow

### Sequence Diagram

```mermaid
sequenceDiagram
    participant main as main.py
    participant MCPClient as MCPClient
    participant MCPServer as mcp_server.py
    participant CliApp as CliApp
    participant CliChat as CliChat
    participant Chat as Chat (base)
    participant Claude as Claude
    participant ToolManager as ToolManager

    main->>MCPClient: Create & connect (stdio)
    MCPClient->>MCPServer: Initialize connection
    main->>CliChat: Create with doc_client, claude_service
    main->>CliApp: Create with CliChat
    CliApp->>CliChat: initialize() - fetch prompts & resources
    
    loop User Input Loop
        CliApp->>CliApp: prompt_async("> ")
        CliApp->>CliChat: run(user_input)
        CliChat->>CliChat: _process_query() or _process_command()
        CliChat->>MCPClient: read_resource() for @mentions
        CliChat->>Chat: run() - agentic loop
        Chat->>ToolManager: get_all_tools()
        Chat->>Claude: chat(messages, tools)
        Claude-->>Chat: response
        alt stop_reason == "tool_use"
            Chat->>ToolManager: execute_tool_requests()
            ToolManager->>MCPClient: call_tool()
            MCPClient->>MCPServer: Execute tool
            MCPServer-->>MCPClient: Result
            Chat->>Claude: Continue with tool results
        end
        Chat-->>CliApp: final_text_response
    end
```

### Key Touchpoints

| Step | File | What Happens |
|------|------|--------------|
| **1. Startup** | `main.py#L26-L59` | Creates `Claude` service, spawns `MCPClient` → `mcp_server.py` via stdio |
| **2. CLI Init** | `core/cli.py#L179-L181` | `CliApp.initialize()` fetches prompts & resources for autocomplete |
| **3. Input Loop** | `core/cli.py#L199-L210` | `prompt_async()` waits for user input, calls `agent.run()` |
| **4. Query Processing** | `core/cli_chat.py#L51-L89` | Handles `/commands` (prompts) or `@mentions` (resources) |
| **5. Agentic Loop** | `core/chat.py#L16-L46` | Loops calling Claude → if `tool_use`, executes tools via `ToolManager` → continues until final response |
| **6. Tool Execution** | `core/tools.py#L53-L106` | Finds correct client, calls MCP tool, returns result to Claude |

---

## What Happens When a Question is Asked

### Sequence Diagram

```mermaid
sequenceDiagram
    participant User
    participant CliApp
    participant CliChat
    participant MCPClient
    participant Claude
    participant ToolManager

    User->>CliApp: Types "Tell me about @deposition.md"
    CliApp->>CliChat: run(query)
    
    Note over CliChat: _process_query()
    CliChat->>CliChat: Check if starts with "/" (command)
    CliChat->>CliChat: Extract @mentions from query
    CliChat->>MCPClient: read_resource("docs://documents/deposition.md")
    MCPClient-->>CliChat: Document content
    CliChat->>CliChat: Build prompt with context
    CliChat->>CliChat: Append to messages[]
    
    Note over CliChat: Agentic Loop (inherited from Chat)
    loop Until stop_reason != "tool_use"
        CliChat->>ToolManager: get_all_tools(clients)
        ToolManager-->>CliChat: [read_doc_contents, edit_document]
        CliChat->>Claude: chat(messages, tools)
        Claude-->>CliChat: Response
        
        alt Claude wants to use a tool
            CliChat->>ToolManager: execute_tool_requests()
            ToolManager->>MCPClient: call_tool("read_doc_contents", {doc_id})
            MCPClient-->>ToolManager: Tool result
            ToolManager-->>CliChat: ToolResultBlockParam
            CliChat->>CliChat: Add tool result to messages[]
        else Claude gives final answer
            CliChat-->>CliApp: final_text_response
        end
    end
    
    CliApp->>User: Print response
```

### Step-by-Step Breakdown

| Step | Location | What Happens |
|------|----------|--------------|
| **1. Input captured** | `core/cli.py#L202` | `prompt_async("> ")` captures user input |
| **2. Run called** | `core/cli.py#L206` | Calls `agent.run(user_input)` |
| **3. Process query** | `core/cli_chat.py#L65-L89` | Extracts `@mentions`, fetches doc content via MCP resource, builds prompt with `<context>` |
| **4. Get tools** | `core/chat.py#L27` | `ToolManager.get_all_tools()` collects tools from all MCP clients |
| **5. Call Claude** | `core/chat.py#L25-L28` | Sends messages + tools to Anthropic API |
| **6. Tool loop** | `core/chat.py#L32-L40` | If Claude returns `stop_reason="tool_use"`, executes tools via MCP, adds results, loops back |
| **7. Final response** | `core/chat.py#L42-L44` | When Claude is done, extracts text and returns |

### Key Insight

**Resources** (`@mentions`) are fetched *before* calling Claude and injected into the prompt, while **tools** are available for Claude to call *during* the conversation loop.
