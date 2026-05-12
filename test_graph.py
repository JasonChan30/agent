from langgraph.graph import StateGraph, START, END
from model import model
from tool.download_video import download_video

tools = [download_video]
tools_by_name = {tool.name: tool for tool in tools}
model_with_tools = model.bind_tools(tools)




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