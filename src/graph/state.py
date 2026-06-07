from langchain.messages import AnyMessage
from typing_extensions import TypedDict, Annotated
import operator

class MessageState(TypedDict):
    messages: list
    query: str
    system_prompt: str

    status: str
    plan: str

    search_result: str
    response: str
