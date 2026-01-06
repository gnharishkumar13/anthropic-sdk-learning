from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic()

model = "claude-sonnet-4-0"

system_prompt = """
You are a math tutor. Do not directly answer a student's question and \
guide the solution with examples
"""

messages: list[dict[str, str]] = []


def add_user_message(messages: list[dict[str, str]], text: str) -> None:
    user_message = {"role": "user", "content": text}
    messages.append(user_message)


def add_assistant_message(messages: list[dict[str, str]], text: str) -> None:
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)


def chat(messages, system=None):
    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messages,
    }

    if system:
        params["system"] = system

    message = client.messages.create(**params)
    return message.content[0].text


while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Exiting the chat.")
        break

    add_user_message(messages, user_input)
    response = chat(messages, system=system_prompt)
    print("Claude:", response)
    add_assistant_message(messages, response)
