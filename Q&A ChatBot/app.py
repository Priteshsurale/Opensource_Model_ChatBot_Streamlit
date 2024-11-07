import os 
from dotenv import load_dotenv
load_dotenv()

os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_PROJECT'] = 'Q&A ChatBOT LLM'


import openai
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from langchain_groq import ChatGroq

# Prompt Template
prompt =  ChatPromptTemplate.from_messages(
    [
        ('system','You are help full assistant. please response to the user queries'),
        ('user','Question:{input}')
    ]
)


def generate_response(question, api_key, llm, temperature, max_token):
    if not api_key:
        return 'ENTER OPEN AI API KEY'
    openai.api_key = api_key
    llm = ChatOpenAI(model=llm,temperature=temperature, max_tokens=max_token)
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    answer = chain.invoke({"input":question})

    return answer


# Title for the app
st.title("Enhance Q&A Chatbot with OpenAI")

# sidebar for setting
st.sidebar.title("Settings")
api_key = st.sidebar.text_input('Enter your OPEN AI API key', type='password')

# Dropdown for select various openai model
llm = st.sidebar.selectbox('Select an Open AI Model',['gpt-4o','gpt-4o-mini','gpt-4-turbo','gpt-3.5-turbo-0125'])

# Adjust response parameter
temperature = st.sidebar.slider('Temperature',max_value=2.0,min_value=0.0,value=1.0) 
max_tokens = st.sidebar.slider('Max_Token',max_value=500,min_value=50,value=150)


# Main Interface For User input
st.write('Go ahead and ask any question')
user_input = st.text_input('You:') 

if user_input:
    response = generate_response(user_input,api_key,llm, temperature,max_tokens)
    st.write(response)
else:
    st.write('Please Provide the Query')