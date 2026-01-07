from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv

client = Anthropic()

model = "claude-sonnet-4-0"
messages: list[dict[str, str]] = []

prompt = """
Generate a sample json for grafana dashboard to check HTTP metrics of a service
"""


def add_user_message(messages, text) -> None:
    user_message = {"role": "user", "content": text}
    messages.append(user_message)


def add_assistant_message(messages, text) -> None:
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)


def chat(messages):
    response = client.messages.create(
        max_tokens=1000,
        model=model,
        messages=messages,
        stop_sequences=["```"],
    )
    return response.content[0].text


add_user_message(messages, prompt)
add_assistant_message(messages, "```json")
answer = chat(messages)
print(answer.strip())
