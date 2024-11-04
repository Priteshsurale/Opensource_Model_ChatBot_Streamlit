from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from fastapi import FastAPI
from langserve import add_routes
import os
from dotenv import load_dotenv
load_dotenv()


groq_api_key = os.getenv('GROQ_API_KEY')


# LLM
model = 'gemma2-9b-it'
llm = ChatGroq(model=model,api_key=groq_api_key)

# Prompt Template
prompt =  ChatPromptTemplate.from_messages(
    [
        ('system','Translate the following into {language}'),
        ('user','{text}')
    ]
)

# parser
parser = StrOutputParser()

# LCEL - LangChain Expression Language  (Chain)
chain = prompt|llm|parser

app = FastAPI(title='Langchain server',
              version='1.0',
              description='A simple API server using langchain runnable interface')


add_routes(
    app,
    chain,
    path='/chain'
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host='localhost',port=8000)