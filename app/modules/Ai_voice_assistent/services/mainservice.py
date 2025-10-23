import re

from langgraph.graph import StateGraph, START, END

#calling tools
from app.modules.Ai_voice_assistent.services.tool.tools import tools, tool_node, get_date_time
#calling agents
from app.modules.Ai_voice_assistent.services.agent.agents import therapist_agent, logical_agent, datetime_agent, classify_message, router, State



# ---------------- Graph ----------------
graph_builder = StateGraph(State)

graph_builder.add_node("classifier", classify_message)

graph_builder.add_node("router", router)

graph_builder.add_node("therapist", therapist_agent)

graph_builder.add_node("logical", logical_agent)

graph_builder.add_node("datetime", datetime_agent)

graph_builder.add_edge(START, "classifier")
graph_builder.add_edge("classifier", "router")
graph_builder.add_conditional_edges(
    "router",
    lambda state: state.get("next"),
    {"therapist": "therapist", "logical": "logical", "datetime": "datetime"}
)
graph_builder.add_edge("therapist", END)
graph_builder.add_edge("logical", END)
graph_builder.add_edge("datetime", END)

graph = graph_builder.compile()

# ________________text cleaning utility ________________
def clean_text(text: str) -> str:
    # Remove newlines
    text = text.replace("\n", " ")
    # Remove special characters (keep letters, numbers, and spaces)
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()
    return text

# ---------------- function calling ----------------
async def agentic_graph(query: str):
    print("Agentic graph invoked")
    state = graph.invoke({"messages": [{"role": "user", "content": query}]})
    text_cleaning = clean_text(state['messages'][-1].content)
    return{"response": text_cleaning}
