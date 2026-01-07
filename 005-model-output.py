from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic()

model = "claude-sonnet-4-0"

messages = []
stop_sequence = ["5"]


def add_user_message(messages, text):
    user_message = {"role": "user", "content": text}
    messages.append(user_message)


def add_assistant_message(messages, text):
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)


def chat(messages, system=None, stop_sequence=None):
    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messages,
    }

    if system:
        params["system"] = system
    if stop_sequence:
        params["stop_sequences"] = stop_sequence

    message = client.messages.create(**params)
    return message.content[0].text


add_user_message(messages, "Is Claude or Codex better for coding?")

# Control the model output by prefilling assistant messages
# add_assistant_message(messages, "Claude is better because")
add_assistant_message(messages, "Codex is really better because")
answer = chat(messages)

print(answer)


# Stop sequences
add_user_message(messages, "Write a list of numbers from 1 to 10, each on a new line.")
answer = chat(messages, None, stop_sequence)
print(answer)
