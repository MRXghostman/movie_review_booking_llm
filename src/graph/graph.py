from langgraph.graph import StateGraph, END
from src.graph.state import MessageState
from src.graph.agents import processing_agent, planner_agent, search_node, booking_node, response_agent, general_chat_agent


def route(state: MessageState):
    if state["plan"] == "search":
        return "search"
    elif state["plan"] == "booking":
        return "booking"
    else:
        return "general"

builder = StateGraph(MessageState)

builder.add_node("processing", processing_agent)
builder.add_node("planner", planner_agent)
builder.add_node("search", search_node)
builder.add_node("booking", booking_node)
builder.add_node("general", general_chat_agent)
builder.add_node("response", response_agent)

builder.set_entry_point("processing")

builder.add_edge("processing", "planner")
builder.add_conditional_edges(
    "planner",
    route,
    {
        "search": "search",
        "booking": "booking",
        "general": "general"
    }
)
builder.add_edge("search", "response")
builder.add_edge("booking", "response")
builder.add_edge("general", END)

app = builder.compile()