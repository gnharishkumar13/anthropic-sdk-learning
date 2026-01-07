from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()


client = Anthropic()

model = "claude-sonnet-4-0"

messages = []


def add_user_message(messages: list[dict[str, str]], text: str) -> None:
    user_message = {"role": "user", "content": text}
    messages.append(user_message)


with client.messages.stream(
    model=model,
    max_tokens=1000,
    messages=[
        {
            "role": "user",
            "content": "Write a joke in a few sentences",
        }
    ],
    system="You are a creative movie director",
    temperature=0.7,
) as stream:
    for text in stream.text_stream:
        # print("-----printing as it streams--------")
        # print(text, end="")
        pass

print("-----final message after streaming--------")
print(stream.get_final_message())
