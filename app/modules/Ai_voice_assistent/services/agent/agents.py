from app.modules.Ai_voice_assistent.services.tool.tools import tools, tool_node, get_date_time
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from typing import Annotated, Literal
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

# Load environment variables
load_dotenv()

# Initialize the LLM (OpenAI GPT)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# ---------------- Models ----------------
class MessageClassifier(BaseModel):
    message_type: Literal["emotional", "logical", "datetime"] = Field(
        ...,
        description="Classify if the message requires an emotional (therapist), logical, or datetime response."
    )

class State(TypedDict):
    messages: Annotated[list, add_messages]
    message_type: str | None
# ---------------- Agents ----------------
def classify_message(state: State):
    last_message = state["messages"][-1]
    classifier_llm = llm.with_structured_output(MessageClassifier)

    result = classifier_llm.invoke([
        {
            "role": "system",
            "content": """Classify the user message as one of:
            - 'emotional': emotional support, therapy, personal problems
            - 'logical': facts, information, analysis, practical solutions
            - 'datetime': asking for current date/time"""
        },
        {"role": "user", "content": last_message.content}
    ])
    return {"message_type": result.message_type}

def router(state: State):
    message_type = state.get("message_type", "logical")
    print(f"Router state: {message_type}")
    if message_type == "emotional":
        return {"next": "therapist"}
    elif message_type == "datetime":
        return {"next": "datetime"}
    return {"next": "logical"}

def therapist_agent(state: State):
    last_message = state["messages"][-1]
    messages = [
        {
            "role": "system",
            "content": """You are a compassionate and empathetic therapist. Your role is to provide emotional support, validate the user's feelings, and give gentle advice if appropriate. 

Guidelines:
1. **Empathy first:** Always acknowledge the user's feelings sincerely. Use phrases like "I hear you," "It makes sense you feel that way," or "That sounds really difficult."
2. **Validation:** Let the user know their emotions are understandable and valid, without judgment.
3. **Advice after listening:** Once the user has shared their problem, provide gentle, supportive, and practical advice tailored to their situation. Do not ask them to explain further or tell you more about their feelings.
4. **Adapt conversation style:** Mirror the user's tone and pace. If they are emotional, respond gently and calmly. If they are casual, keep a warm and conversational tone.
5. **Closure:** If the conversation is winding down, offer comforting closure statements.

Example responses:
- *"I hear you. That sounds really challenging. One approach that might help is… [gentle advice]."*
- *"It makes sense you feel that way. You could try… [supportive suggestion]."*
- *"I understand how upsetting that must be. A helpful step could be… [practical guidance]."*

Remember: **Your main goal is emotional support, validation, and then providing advice without asking for more details.**
."""
        },
        {"role": "user", "content": last_message.content}
    ]
    reply = llm.invoke(messages)
    return {"messages": [{"role": "assistant", "content": reply.content}]}

def logical_agent(state: State):
    last_message = state["messages"][-1]
    messages = [
        {
            "role": "system",
            "content": """You are a purely logical assistant. 
            Always use the 'tavily_search' tool to answer questions. 
            Never answer from your own knowledge."""
        },
        {"role": "user", "content": last_message.content}
    ]
    tool_call = llm.bind_tools(tools).invoke(messages)

    if hasattr(tool_call, "tool_calls") and tool_call.tool_calls:
        tool_results = tool_node.invoke({"messages": [tool_call]})
        return {"messages": [tool_results["messages"][-1]]}
    return {"messages": [{"role": "assistant", "content": tool_call.content}]}

def datetime_agent(state: State):
    tool_call = llm.bind_tools(tools).invoke([
        {
            "role": "system",
            "content": "Always use the get_date_time tool to provide the current date and time."
        },
        {"role": "user", "content": "What is the current date and time?"}
    ])

    if tool_call.tool_calls:
        tool_results = tool_node.invoke({"messages": [tool_call]})
        tool_message = tool_results["messages"][-1]
        final_response = f"The current date and time is: {tool_message.content}"
        return {"messages": [{"role": "assistant", "content": final_response}]}

    return {"messages": [{"role": "assistant", "content": get_date_time()}]}
