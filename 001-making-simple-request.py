from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic()

model = "claude-sonnet-4-0"

message = client.messages.create(
    model=model,
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude!"},
    ],
)

print(message.content[0].text)
