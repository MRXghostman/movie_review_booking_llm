from src.graph.state import MessageState
from src.llm.ollama_client import ollama_chat


def processing_agent(state: MessageState) -> MessageState:
    # Simulate processing the message
    if state["query"]:
        return {"status": "processing"}
    else:
        return {"status": "error"}
    
def planner_agent(state: MessageState) -> MessageState:
    messages = [
        {
            "role": "system",
            "content": """
        You are a classifier.
        based on the use prompt, classify the user's intent into one of three categories: Search, Booking, or General.
        Rules:
        - Return exactly one word.
        - Do not explain.
        - Do not greet.
        - Do not answer the user.

        Valid outputs:
        Search
        Booking
        General

        Anything else is invalid.
        """
        },
        {
            "role": "user",
            "content": state["query"]
        }
    ]

    plan = ollama_chat(messages).strip()
    return {"status": "planning", "plan": plan.lower()}

def general_chat_agent(state: MessageState) -> MessageState:
    messages = [
        {
            "role": "system", "content": state["system_prompt"]
        },
    ]
    messages.extend(state["messages"])

    messages.append(
        {
            "role": "user", "content": state["query"]
        }
    )
    

    response = ollama_chat(messages)

    return {"status": "responding", "response": response }

def search_node(state: MessageState):

    return {
        "status": "searching",
        "search_result": (
            f"Search results for: {state['query']}"
        )
    }


def booking_node(state: MessageState):

    return {
        "status": "booking",
        "search_result": (
            f"Booking workflow for: {state['query']}"
        )
    }

def response_agent(state:MessageState) -> MessageState:
    messages = [
        {
            "role": "system", "content": state["system_prompt"]
        },
    ]
    messages.extend(state["messages"])

    messages.append(
        {
            "role": "user", "content": state["query"]
        }
    )
    

    response = ollama_chat(messages)

    return {"status": "responding", "response": response }