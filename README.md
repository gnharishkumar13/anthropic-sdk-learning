### Setup

- Install uv
- Initilize the project `uv init`
- Add dependencies with `uv add <package-name>` command. For example: `uv add anthropic`
- Run the programs with `uv run file-name`
- Set Python Interpreter in VScode to `uv`

### Notes

SDK https://platform.claude.com/docs/en/agent-sdk/overview

#### Messages API

https://platform.claude.com/docs/en/build-with-claude/working-with-messages

The core of making API requests is the **client.messages.create()** function. This function requires three key parameters:

- model - The name of the Claude model you want to use
- max_tokens - A safety limit on response length (not a target)
- messages - The conversation history you're sending to Claude

Understanding messages

- User messages - Content you want to send to Claude (written by humans)
- Assistant messages - Responses that Claude has generated
