import os

from dotenv import load_dotenv
from langchain_community.chat_models import ChatZhipuAI

load_dotenv()

import operator
from typing import Annotated, Literal, TypedDict

from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


# 1. Define tools and model
model = ChatZhipuAI(
    zhipuai_api_key=os.getenv("ZHIPUAI_API_KEY"),
    model="glm-4.7"
)

@tool
def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b

@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b

@tool
def divide(a: float, b: float) -> float:
    """Divide two numbers."""
    return a / b

tools = [add, multiply, divide]
tools_by_name = {tool.name: tool for tool in tools}
model_with_tools = model.bind_tools(tools)


# 2. Define state
class MessagesState(TypedDict):
    messages: Annotated[list, add_messages]
    llmCalls: int


# 3. Define model node
def llm_call(state: MessagesState):
    response = model_with_tools.invoke(
        [
            SystemMessage(
                content="You are a helpful assistant tasked with performing arithmetic on a set of inputs."
            ),
            *state["messages"],
        ]
    )
    return {
        "messages": [response],
        "llmCalls": 1,
    }


# 4. Define tool node
def tool_node(state: MessagesState):
    last_message = state["messages"][-1] if state["messages"] else None

    if last_message is None or not isinstance(last_message, AIMessage):
        return {"messages": []}

    results = []
    for tool_call in last_message.tool_calls or []:
        tool_fn = tools_by_name[tool_call["name"]]
        observation = tool_fn.invoke(tool_call)
        results.append(observation)

    return {"messages": results}


# 5. Define end logic
def should_continue(state: MessagesState) -> Literal["toolNode", "__end__"]:
    last_message = state["messages"][-1] if state["messages"] else None

    if not isinstance(last_message, AIMessage):
        return END

    if last_message.tool_calls:
        return "toolNode"

    return END


# 6. Build and compile the agent
graph = StateGraph(MessagesState)
graph.add_node("llmCall", llm_call)
graph.add_node("toolNode", tool_node)
graph.add_edge(START, "llmCall")
graph.add_conditional_edges("llmCall", should_continue, ["toolNode", END])
graph.add_edge("toolNode", "llmCall")

agent = graph.compile()

# Invoke
result = agent.invoke(
    {
        "messages": [HumanMessage(content="Add 3 and 4.")],
        "llmCalls": 0,
    }
)

for message in result["messages"]:
    print(f"[{message.type}]: {message.content}")