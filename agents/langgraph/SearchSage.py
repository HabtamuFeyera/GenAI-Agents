from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from IPython.display import Image


# Define AgentState using TypedDict
class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]

# Define the SearchSage Agent class
class SearchSage:

    def __init__(self, model, tools, system=""):
        self.system = system
        graph = StateGraph(AgentState)
        
        # Add nodes to the graph (states in the workflow)
        graph.add_node("llm", self.call_openai)
        graph.add_node("action", self.take_action)
        
        # Add conditional edges based on action existence
        graph.add_conditional_edges(
            "llm",
            self.exists_action,
            {True: "action", False: END}
        )
        
        # Loop between the action and llm states
        graph.add_edge("action", "llm")
        graph.set_entry_point("llm")
        
        self.graph = graph.compile()
        
        # Set tools and bind them to the model
        self.tools = {t.name: t for t in tools}
        self.model = model.bind_tools(tools)

    # Check if there are actions in the last message
    def exists_action(self, state: AgentState):
        result = state['messages'][-1]
        return len(result.tool_calls) > 0

    # Call the OpenAI model
    def call_openai(self, state: AgentState):
        messages = state['messages']
        if self.system:
            messages = [SystemMessage(content=self.system)] + messages
        message = self.model.invoke(messages)
        return {'messages': [message]}

    # Perform the actions based on the tool calls
    def take_action(self, state: AgentState):
        tool_calls = state['messages'][-1].tool_calls
        results = []
        for t in tool_calls:
            print(f"Calling: {t}")
            if not t['name'] in self.tools:  # check for invalid tool name
                print("\n ....bad tool name....")
                result = "bad tool name, retry"  # instruct LLM to retry
            else:
                result = self.tools[t['name']].invoke(t['args'])
            results.append(ToolMessage(tool_call_id=t['id'], name=t['name'], content=str(result)))
        
        print("Back to the model!")
        return {'messages': results}

# Define the prompt (system message)
prompt = """You are a smart research assistant. Use the search engine to look up information. \
You are allowed to make multiple calls (either together or in sequence). \
Only look up information when you are sure of what you want. \
If you need to look up some information before asking a follow-up question, you are allowed to do that!
"""

# Note, the query was modified to produce more consistent results. 
# Results may vary per run and over time as search information and models change.
query = """Who won the super bowl in 2024? In what state is the winning team headquarters located? \
What is the GDP of that state? Answer each question."""

# Create the messages list with the query
messages = [HumanMessage(content=query)]

# Initialize the more advanced model (gpt-4o)
model = ChatOpenAI(model="gpt-4o")  # Use a more advanced model

# Initialize the search tool (you can configure other tools here as well)
tool = TavilySearchResults(max_results=4)  # Allow up to 4 results

# Instantiate the SearchSage agent with the model, tools, and prompt
search_sage = SearchSage(model, [tool], system=prompt)

# Invoke the agent with the query and get the result
result = search_sage.graph.invoke({"messages": messages})

# Print out the agent's response
print(result)

# Render and display the graph as a PNG
try:
    # Generate the PNG image of the graph
    graph_image = search_sage.graph.get_graph().draw_png()  # If this method is available
    
    # Display the generated PNG image
    Image(graph_image)
except AttributeError:
    # If 'get_graph().draw_png()' is not available, try using Graphviz directly
    print("Rendering graph using graphviz...")
    
    # Generate DOT format and render using Graphviz
    dot = graphviz.Source(search_sage.graph.get_graph().to_dot())  # Get DOT format from the graph
    dot.render('graph_output', format='png', cleanup=True)  # Save to PNG file
    
    # Display the generated PNG image
    Image('graph_output.png')
