from ollama import chat

def ollama_chat(message):
    response = chat(messages=message, model="llama3.1")
    return response["message"]["content"]
