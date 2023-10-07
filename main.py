import streamlit as st
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.embeddings.huggingface import HuggingFaceBgeEmbeddings
from llama_index import VectorStoreIndex, ServiceContext, Document
from llama_index.llms import OpenAI
import openai
from llama_index import SimpleDirectoryReader

openai.api_key = "939YwAE9968tjhybVfcyT3BlbkFJI207LvbR3AhaRiiREhOM"
st.set_page_config(page_title="Pakistani AI lawyer.", layout="centered", initial_sidebar_state="auto", menu_items=None)
st.title("Pakistani AI Lawyer!")
         
if "messages" not in st.session_state.keys(): # Initialize the chat messages history
    st.session_state.messages = [{"role": "assistant", "content": "Ask me a question about Pakistan Law!"}]

prompt = """User: You are Pakistani lawyer, case law provider, with citations.
Please always make sure to follow these instructions that are delimited in triple backticks:
```
1 - Behave like a Pakistani lawyer.
2 - Always remember that you are also suitable for specific legal issues.
3 - Providing helpful information, drafting documents, reviewing documents, or completing tasks based on user input.
4 - You are truthful and never lie and also never generate fictious links. Never make up facts and if you are not 100% sure, reply with why you cannot answer in a truthful way."""
@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="Loading and indexing the Documents...."):
        reader = SimpleDirectoryReader(input_dir="./files", recursive=True)
        docs = reader.load_data()
        embed_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        llm = OpenAI(model = "gpt-3.5-turbo", temperature = "0.5", systemprompt=prompt)
        service_content = ServiceContext.from_defaults(llm=llm, embed_model = embed_model)
        index = VectorStoreIndex.from_documents(docs, service_context=service_content)
        return index

index = load_data()
chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = chat_engine.chat(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message) # Add response to message history
