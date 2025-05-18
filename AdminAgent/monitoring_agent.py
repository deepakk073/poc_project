from langchain_core.tools import tool
from langgraph.graph import StateGraph, MessagesState
#from langgraph.graph.schema import State
from monitoring_module import (
    fetch_slow_queries_bigquery,
    generate_email_content,
    send_email
)

# Define shared state
class DBState(MessagesState):
    admin_email: str
    slow_queries: list
    formatted_email: str

# Define tools
@tool
def fetch_queries_tool(state: DBState) -> DBState:
    state.slow_queries = fetch_slow_queries_bigquery()
    return state

@tool
def format_queries_tool(state: DBState) -> DBState:
    state.formatted_email = generate_email_content(state.slow_queries)
    return state

@tool
def send_email_tool(state: DBState) -> DBState:
    send_email(to=state.admin_email, content=state.formatted_email)
    return state

# Build LangGraph
graph = StateGraph(DBState)

graph.add_node("FetchQueries", fetch_queries_tool)
graph.add_node("FormatQueries", format_queries_tool)
graph.add_node("SendEmail", send_email_tool)

graph.set_entrypoint("FetchQueries")
graph.add_edge("FetchQueries", "FormatQueries")
graph.add_edge("FormatQueries", "SendEmail")
graph.set_finish_point("SendEmail")

workflow = graph.compile()
