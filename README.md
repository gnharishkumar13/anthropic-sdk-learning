### Setup

- Install uv
- Initilize the project `uv init`
- Add dependencies with `uv add <package-name>` command. For example: `uv add anthropic`
- Run the programs with `uv run file-name`
- Set Python Interpreter in VScode to `uv`

### Notes

SDK https://platform.claude.com/docs/en/agent-sdk/overview

### Claude API

#### Messages API

https://platform.claude.com/docs/en/build-with-claude/working-with-messages

The core of making API requests is the **client.messages.create()** function. This function requires three key parameters:

- model - The name of the Claude model you want to use
- max_tokens - A safety limit on response length (not a target)
- messages - The conversation history you're sending to Claude

##### Understanding messages

- User messages - Content you want to send to Claude (written by humans)
- Assistant messages - Responses that Claude has generated

###### Stateless conversation

Claude does not remember previous messages in a conversation. Each message is treated as a new conversation.

Multi-Turn conversations:

- Add the assistant message to the user message and convert it to to a loop conversation

#### System Prompts

Assign a persona to the LLM model by adding a system prompt at the start of the messages array.
System

#### Temperature

- Temperature is a powerful parameter that controls how predictable or creative Claude's responses will be. Understanding how to use it effectively can dramatically improve your AI applications.
- Temperature is a decimal value between 0 and 1 that directly influences these selection probabilities. It's like adjusting the "creativity dial" on Claude's responses.

Tokenization - Breaking your input into smaller chunks
Prediction - Calculating probabilities for possible next words
Sampling - Choosing a token based on those probabilities

At low temperatures (near 0), Claude becomes very deterministic - it almost always picks the highest probability token. At high temperatures (near 1), Claude distributes probability more evenly across options, leading to more varied and creative outputs.

```
# Low temperature - more predictable
answer = chat(messages, temperature=0.0)

# High temperature - more creative
answer = chat(messages, temperature=1.0)
```

#### Response Streaming

With streaming enabled, Claude immediately sends back an initial response indicating it has received your request and is starting to generate text. Then you receive a series of events, each containing a small piece of the overall response.

##### Stream Events

Claude sends back several types of events:

- MessageStart - A new message is being sent
- ContentBlockStart - Start of a new block containing text, tool use, or other content
- ContentBlockDelta - Chunks of the actual generated text
- ContentBlockStop - The current content block has been completed
- MessageDelta - The current message is complete
- MessageStop - End of information about the current message

The **ContentBlockDelta** events contain the actual generated text to display to users.

```
with client.messages.stream(
    model=model,
    max_tokens=1000,
    messages=messages
) as stream:
    for text in stream.text_stream:
        # Send each chunk to client
        pass

    # Get the complete message for database storage
    final_message = stream.get_final_message()
```

#### Controlling Model output

- Prefilled Assistant Messages (The key thing to understand is that \
  Claude continues from exactly where prefilled text ends.)
- Stop sequences

```
messages = []
add_user_message(messages, "Count from 1 to 10")
answer = chat(messages, stop_sequences=["5"])
```

#### Structured data

````
messages = []

add_user_message(messages, "Generate a very short event bridge rule as json")
add_assistant_message(messages, "```json")

text = chat(messages, stop_sequences=["```"])
````

This will work for other formats Also

- Python code snippets
- Bulleted lists
- CSV data
- Any formatted content where you want just the content, not explanations

Also, in beta:

> https://platform.claude.com/docs/en/build-with-claude/structured-outputs

### Prompting

####
