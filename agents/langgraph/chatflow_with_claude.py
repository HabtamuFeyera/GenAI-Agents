from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_anthropic import ChatAnthropic
from IPython.display import Image, display

# Step 1: Define the State for the conversation
class State(TypedDict):
    messages: Annotated[list, add_messages]  # Conversation history will be stored here

# Step 2: Create an instance of the StateGraph, passing in the State class
graph_builder = StateGraph(State)

# Step 3: Initialize LangChain's Claude model
llm = ChatAnthropic(model="claude-3-5-sonnet-20240620")

# Step 4: Define the chatbot node function
def chatbot(state: State):
    # Use the LLM to generate a response based on the current conversation history
    response = llm.invoke(state["messages"])

    # Return the updated state with the new message appended
    return {"messages": state["messages"] + [{"role": "assistant", "content": response}]}

# Step 5: Add the 'chatbot' node to the graph
graph_builder.add_node("chatbot", chatbot)

# Step 6: Set up transitions: From START to 'chatbot', and from 'chatbot' to END
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

# Compile the graph
graph = graph_builder.compile()

# Optional: Visualize the graph as a Mermaid diagram (requires extra dependencies)
try:
    display(Image(graph.get_graph().draw_mermaid_png()))
except Exception:
    print("Graph visualization is optional and requires extra dependencies.")

# Step 7: Main loop for user interaction
while True:
    user_input = input("User: ").strip()
    
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
        break

    # Process user input through the LangGraph
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
        for value in event.values():
            print("Assistant:", value["messages"][-1]["content"])  # Print the assistant's last response
