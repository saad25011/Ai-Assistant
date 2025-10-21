from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()

# Initialize the LLM (OpenAI GPT)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
# ---------------- Tools ----------------
@tool
def get_date_time() -> str:
    """Get the current date and time in a formatted string."""
    date = datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
    return date

@tool
def tavily_search(query: str) -> str:
    """Fetch latest data from Tavily search and return as a string."""
    search = TavilySearchResults(max_results=3)

    results = search.run(query)

    result_str = "\n\n".join(
        [f"Title: {r['title']}\nURL: {r['url']}\nContent: {r['content'][:300]}..." for r in results]
    )

    # Summarize with OpenAI LLM
    summary = llm.invoke([
        {
            "role": "system",
            "content": "Summarize the search results into 1-2 factual sentences, concise and clear."
        },
        {"role": "user", "content": result_str}
    ])


    print(f"Search results summary: {summary.content}")


    return summary.content

tools = [get_date_time, tavily_search]

tool_node = ToolNode(tools)
