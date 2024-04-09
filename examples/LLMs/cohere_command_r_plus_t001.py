
import os
os.environ["COHERE_API_KEY"] = COHERE_API_KEY

# ==========================================================

# You can easily equip your agent with web search!

from langchain_community.tools.tavily_search import TavilySearchResults

os.environ["TAVILY_API_KEY"] = TAVILY_API_KEY

internet_search = TavilySearchResults()
internet_search.name = "internet_search"
internet_search.description = "Returns a list of relevant document snippets for a textual query retrieved from the internet."


from langchain_core.pydantic_v1 import BaseModel, Field
class TavilySearchInput(BaseModel):
   query: str = Field(description="Query to search the internet with")
internet_search.args_schema = TavilySearchInput


# ==========================================================

# You can easily equip your agent with a Python interpreter!

from langchain.agents import Tool
from langchain_experimental.utilities import PythonREPL

python_repl = PythonREPL()
python_tool = Tool(
   name="python_repl",
   description="Executes python code and returns the result. The code runs in astatic sandbox without interactive mode, so print output or save output to a file.",
   func=python_repl.run,
)
python_tool.name = "python_interpreter"

# from langchain_core.pydantic_v1 import BaseModel, Field
class ToolInput(BaseModel):
   code: str = Field(description="Python code to execute.")
python_tool.args_schema = ToolInput

# ==========================================================


from langchain_core.tools import tool
import random

@tool
def random_operation_tool(a: int, b: int):
 """Calculates a random operation between the inputs."""
 coin_toss = random.uniform(0, 1)
 if coin_toss > 0.5:
   return {'output': a*b}
 else:
   return {'output': a+b}

random_operation_tool.name = "random_operation" # use python case
random_operation_tool.description = "Calculates a random operation between the inputs."

from langchain_core.pydantic_v1 import BaseModel, Field
class random_operation_inputs(BaseModel):
   a: int = Field(description="First input")
   b: int = Field(description="Second input")
random_operation_tool.args_schema = random_operation_inputs



# ==========================================================
# You can easily equip your agent with a vector store!

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_cohere import CohereEmbeddings

# Set embeddings
embd = CohereEmbeddings()

# Docs to index
urls = [
   "https://paulgraham.com/best.html",
]

# Load
docs = [WebBaseLoader(url).load() for url in urls]
docs_list = [item for sublist in docs for item in sublist]

# Split
text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
   chunk_size=512, chunk_overlap=0
)
doc_splits = text_splitter.split_documents(docs_list)

# Add to vectorstore
vectorstore = FAISS.from_documents(
   documents=doc_splits,
   embedding=embd,
)

vectorstore_retriever = vectorstore.as_retriever()


from langchain.tools.retriever import create_retriever_tool

vectorstore_search = create_retriever_tool(
   retriever=vectorstore_retriever,
   name="vectorstore_search",
   description="Retrieve relevant info from a vectorstore that contains information from Paul Graham about how to write good essays."
)
# ==========================================================

from langchain.agents import AgentExecutor
from langchain_cohere.react_multi_hop.agent import create_cohere_react_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_cohere.chat_models import ChatCohere

# LLM
llm = ChatCohere(model="command-r-plus", temperature=0.3)

# Preamble
preamble = """
You are an expert who answers the user's question with the most relevant datasource.
You are equipped with an internet search tool and a special vectorstore of information
about how to write good essays.
"""

# Prompt template
prompt = ChatPromptTemplate.from_template("{input}")

# Create the ReAct agent
agent = create_cohere_react_agent(
   llm=llm,
   tools=[internet_search, vectorstore_search, python_tool],
   prompt=prompt,
)

agent_executor = AgentExecutor(agent=agent,
                               tools=[internet_search, vectorstore_search, python_tool],
                               verbose=True)


# ==========================================================
agent_executor.invoke({
   "input": "I want to write an essay about the Roman Empire. Any tips for writing an essay? Any fun facts?",
   "preamble": preamble,
})

# ==========================================================

# Step 1: Construct the chat history as a list of LangChain Messages, ending with the last user message
from langchain_core.messages import HumanMessage, AIMessage

chat_history = [
   HumanMessage(content="I'm considering switching to Oracle for my CRM."),
   AIMessage(content="That sounds like a good idea! How can I help you?"),
   HumanMessage(content="Recap all the info you can find about their offering."),
]

prompt = ChatPromptTemplate.from_messages(chat_history)

# Step 2: When you make the agent, specify the chat_history as the prompt
agent = create_cohere_react_agent(
   llm=llm,
   tools=[internet_search, vectorstore_search, python_tool],
   prompt=prompt,
)

agent_executor = AgentExecutor(agent=agent,
                               tools=[internet_search, vectorstore_search, python_tool],
                               verbose=True)

# Step 3: When you invoke the agent_executor there's no need to pass anything else into invoke
response = agent_executor.invoke({
   "preamble": preamble,
})

response['output']

# ==========================================================
# directly_answer
agent_executor.invoke({
   "input": "Hey how are you?",
})

# ==========================================================