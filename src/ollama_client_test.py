from llm.ollama_client import ollama_chat

def test_ollama_chat():
    message = [{
        "role": "system",
        "content": "You are a helpful assistant for movie recommendations."
    }, {
        "role": "user",
        "content": "Find me some good movies for this weekend."
    }]

    response = ollama_chat(message)
    print("Ollama Response:", response)
    assert isinstance(response, str)
    assert len(response) > 0

test_ollama_chat()