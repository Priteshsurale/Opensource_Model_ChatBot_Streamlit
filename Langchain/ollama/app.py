import streamlit as st
import os 
from dotenv import load_dotenv
load_dotenv()

from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

## Langsmith Tracking
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_PROJECT"]=os.getenv("LANGCHAIN_PROJECT")


st.title('Langchain Demo With OpenSource Model')

model = st.selectbox('Select The Model:',['gemma2:9b','llama3:instruct','llama3.2:latest','llama3.1:latest'])

llm = OllamaLLM(model=model)

prompt = ChatPromptTemplate.from_messages(
    [
        ('system','You are a helpful assistant, please answer to the question asked!'),
        ('user','Question:{question}')
    ]
)

output_parser = StrOutputParser()

input_text = st.text_input('What in Your Mind?')


chain = prompt|llm|output_parser

if input_text:
    st.write(chain.invoke({'question':input_text}))