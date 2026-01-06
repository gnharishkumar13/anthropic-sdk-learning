from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()


client = Anthropic()

model = "claude-sonnet-4-0"

# stateless conversations
message = client.messages.create(
    model=model,
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "What is Photosynthesis?"},
    ],
)

print(message.content[0].text)


message = client.messages.create(
    model=model,
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Write one more sentence"},
    ],
)

# stateless conversations

print("---------second message---------")
print(message.content[0].text)


# Multi Turn conversations:


print("--------- Multi Turn conversations: -----------")


def add_user_message(messages, text):
    user_message = {"role": "user", "content": text}
    messages.append(user_message)


def add_assistant_message(messages, text):
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)


def chat(messages):
    message = client.messages.create(
        model=model,
        max_tokens=1000,
        messages=messages,
    )
    return message.content[0].text


# Start with an empty message list
messages = []

# Add the initial user question
add_user_message(messages, "What is Photosynthesis?")

# Get Claude's response
answer = chat(messages)
print(answer)

# Add Claude's response to the conversation history
add_assistant_message(messages, answer)

# Add a follow-up question
add_user_message(messages, "Write another sentence")

# Get the follow-up response with full context
final_answer = chat(messages)
print("-------final_answer--------------")
print(final_answer)


# convert it to loop using while loop
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Exiting the chat.")
        break

    add_user_message(messages, user_input)
    response = chat(messages)
    print("Claude:", response)
    add_assistant_message(messages, response)
