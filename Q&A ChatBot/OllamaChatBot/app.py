import os 
from dotenv import load_dotenv
load_dotenv()


os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_PROJECT'] = 'Q&A ChatBOT LLM with Ollama'


import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

prompt = ChatPromptTemplate.from_messages(
    [
        ('system','You are help full assistant. please response to the user queries'),
        ('user','Question:{input}')
    ]
)


def generate_response(question, model, temperature, max_token):
    llm = ChatOllama(model=model,temperature=temperature, max_tokens=max_token)
    
    # llm = ChatGroq(model='llama3-8b-8192',api_key=os.getenv('GROQ_API_KEY'), temperature=temperature,max_tokens=max_token)
    parser = StrOutputParser()
    
    chain = prompt | llm | parser
    
    response = chain.invoke({'input':question})
    
    return response



# Title for the app
st.title("Enhance Q&A Chatbot with OpenAI")

# sidebar for setting 
st.sidebar.title('Settings')

llm = st.sidebar.selectbox('Select an OpenSource Model',['gemma2:9b','llama3:instruct','llama3.2:latest','llama3.1:latest'])

temperature = st.sidebar.slider('Temperature',max_value=2.0,min_value=0.0,value=1.0) 
max_tokens = st.sidebar.slider('Max_Token',max_value=500,min_value=50,value=150)


# Main Interface For User input
st.write('Go ahead and ask any question')
user_input = st.text_input('You:') 

if user_input:
    response = generate_response(user_input,llm, temperature,max_tokens)
    st.write(response)
else:
    st.write('Please Provide the Query')















