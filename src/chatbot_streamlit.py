import openai
import re
import httpx
import os
import ast
from bs4 import BeautifulSoup
import streamlit as st

# Retrieve the OpenAI API key from environment variable for security
openai.api_key = os.getenv("OPENAI_API_KEY")  # Ensure you've set the OPENAI_API_KEY environment variable

if not openai.api_key:
    raise ValueError("API key not set. Please set the OPENAI_API_KEY environment variable.")

class ChatBot:
    def __init__(self, system=""):
        self.system = system
        self.messages = []
        if self.system:
            self.messages.append({"role": "system", "content": self.system})

    def __call__(self, message):
        self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result

    def execute(self):
        try:
            # Make an API call to OpenAI using the chat model endpoint
            completion = openai.ChatCompletion.create(
                model="gpt-4",
                messages=self.messages  # Send the full conversation as messages
            )
            return completion['choices'][0]['message']['content']
        except Exception as e:
            return f"Error during OpenAI API call: {e}"

# Define the prompt with the behavior of the assistant
prompt = """
You run in a loop of Thought, Action, PAUSE, Observation.
At the end of the loop you output an Answer.
Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Observation will be the result of running those actions.

Your available actions are:

calculate:
e.g. calculate: 4 * 7 / 3
Runs a calculation and returns the number - uses Python so be sure to use floating point syntax if necessary

wikipedia:
e.g. wikipedia: Django
Returns a summary from searching Wikipedia

simon_blog_search:
e.g. simon_blog_search: Django
Search Simon's blog for that term

Always look things up on Wikipedia if you have the opportunity to do so.

Example session:

Question: What is the capital of France?
Thought: I should look up France on Wikipedia.
Action: wikipedia: France
PAUSE

You will be called again with this:

Observation: France is a country. The capital is Paris.

You then output:

Answer: The capital of France is Paris
""".strip()

# Regular expression to match the action syntax in the response
action_re = re.compile(r'^Action: (\w+): (.*)$')

def query(question, max_turns=5):
    i = 0
    bot = ChatBot(prompt)
    next_prompt = question
    while i < max_turns:
        i += 1
        result = bot(next_prompt)
        actions = [action_re.match(a) for a in result.split('\n') if action_re.match(a)]
        if actions:
            # There is an action to run
            action, action_input = actions[0].groups()
            if action not in known_actions:
                raise Exception(f"Unknown action: {action}: {action_input}")
            observation = known_actions[action](action_input)
            next_prompt = f"Observation: {observation}"
        else:
            return result

# Wikipedia search function
def wikipedia(q):
    try:
        response = httpx.get("https://en.wikipedia.org/w/api.php", params={
            "action": "query",
            "list": "search",
            "srsearch": q,
            "format": "json"
        })
        response.raise_for_status()  # Ensure the request was successful
        search_results = response.json()["query"]["search"]
        if search_results:
            snippet = search_results[0]["snippet"]
            clean_snippet = BeautifulSoup(snippet, "html.parser").get_text()
            return clean_snippet
        else:
            return "No results found on Wikipedia."
    except httpx.RequestError as e:
        return f"Error while fetching Wikipedia data: {e}"

# Blog search function for Simon's blog
def simon_blog_search(q):
    try:
        response = httpx.get("https://datasette.simonwillison.net/simonwillisonblog.json", params={
            "sql": """
            select
              blog_entry.title || ': ' || substr(html_strip_tags(blog_entry.body), 0, 1000) as text,
              blog_entry.created
            from
              blog_entry join blog_entry_fts on blog_entry.rowid = blog_entry_fts.rowid
            where
              blog_entry_fts match escape_fts(:q)
            order by
              blog_entry_fts.rank
            limit
              1""".strip(),
            "_shape": "array",
            "q": q,
        })
        response.raise_for_status()  # Ensure the request was successful
        if response.json():
            return response.json()[0]["text"]
        else:
            return "No relevant blog posts found."
    except httpx.RequestError as e:
        return f"Error while fetching blog data: {e}"

# Safe calculation function
def calculate(what):
    try:
        # Validate only mathematical expressions are being evaluated
        if not re.match(r'^[\d+\-*/().\s]+$', what):
            return "Invalid calculation: Non-mathematical characters detected."
        return ast.literal_eval(what)
    except (ValueError, SyntaxError) as e:
        return f"Invalid calculation: {e}"

# Dictionary of known actions for easy lookup
known_actions = {
    "wikipedia": wikipedia,
    "calculate": calculate,
    "simon_blog_search": simon_blog_search
}

# Streamlit UI
def main():
    # Custom CSS to style the page
    st.markdown("""
        <style>
            body {
                background-color: #f4f7fa;
                font-family: 'Arial', sans-serif;
            }
            .stButton>button {
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                padding: 10px 20px;
                border-radius: 5px;
                border: none;
            }
            .stButton>button:hover {
                background-color: #45a049;
            }
            .stTextInput>div>input {
                font-size: 16px;
                padding: 10px;
                border-radius: 5px;
                width: 100%;
                border: 2px solid #ccc;
            }
            .stTextInput>div>input:focus {
                border-color: #4CAF50;
            }
            .stMarkdown {
                font-size: 18px;
                font-weight: 500;
                line-height: 1.6;
            }
            .stSpinner>div>div {
                display: flex;
                justify-content: center;
            }
        </style>
    """, unsafe_allow_html=True)

    # Sidebar for explanation about agents and architecture
    st.sidebar.title("About the System")
    st.sidebar.markdown("""
    ### Agents and Architecture
    This AI chatbot is powered by **OpenAI's GPT-4**. It is designed to interact with users in a loop of:
    - **Thought**: Describes the reasoning process for solving the user's question.
    - **Action**: Executes a specific action like calculating, searching Wikipedia, or querying Simon's blog.
    - **PAUSE**: Waits for the action's result.
    - **Observation**: Provides the result of the executed action, which is then returned as the answer.

    The chatbot utilizes a set of predefined actions, including:
    - **Wikipedia Search**: Queries Wikipedia for related content.
    - **Simon Blog Search**: Queries Simon's blog for relevant posts.
    - **Calculation**: Performs safe mathematical calculations.

    ### Contact Information
    **Habtamu Feyera**  
    - Email: [habtamufeyera95@gmail.com](mailto:habtamufeyera95@gmail.com)
    - LinkedIn: [Habtamu Feyera](https://www.linkedin.com/in/habtamu-feyera)
    - Telegram: [@DecodeAI](https://t.me/DecodeAI)

    """)

    st.title("AI ChatBot with Streamlit")
    st.write("Ask any question and get answers via AI powered by OpenAI's GPT-4!")

    # Initialize session state if not already present
    if 'conversation' not in st.session_state:
        st.session_state.conversation = []

    # Display past conversation
    for idx, message in enumerate(st.session_state.conversation):
        role = message.get('role', 'user')
        st.markdown(f"**{role.capitalize()}:** {message['content']}")

    # User input
    question = st.text_input("Ask a question:", "")

    if question:
        # Process the input and get a response
        with st.spinner("Processing your question..."):
            response = query(question)
        
        # Append the question and answer to session state
        st.session_state.conversation.append({"role": "user", "content": question})
        st.session_state.conversation.append({"role": "assistant", "content": response})

        # Display the response
        st.markdown(f"**Assistant:** {response}")


if __name__ == "__main__":
    main()
