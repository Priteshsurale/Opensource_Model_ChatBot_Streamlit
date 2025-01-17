import os
from dotenv import load_dotenv
load_dotenv()


import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_history_aware_retriever, create_retrieval_chain

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

os.environ["HF_TOKEN"] = os.getenv('HF_TOKEN')
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


st.title('Conversational RAG with PDF uploads and chat History')
st.write('uploads PDF\'s and chat with their content')

api_key= st.text_input('Enter you Groq api key', type='password')


if api_key:
    llm = ChatGroq(model='Gemma2-9b-It',api_key=api_key)
    
    session_id = st.text_input('Session ID',value='default_session')
    
    if 'store' not in st.session_state:
        st.session_state.store = {}
    
    upload_files = st.file_uploader('Choose PDF files', type='pdf', accept_multiple_files=True)
    
    if upload_files:
        documents = []
        for upload_file in upload_files:
            tempdf = './temp.pdf'
            
            with open(tempdf,'wb') as file:
                file.write(upload_file.getvalue())
                file_name = upload_file.name
                
            loader = PyPDFLoader(tempdf)
            doc = loader.load()
            documents.extend(doc)
            
            # split and create embedding for the documents
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000,chunk_overlap=500)
            splits = text_splitter.split_documents(documents)
            vectorstore = FAISS.from_documents(documents=splits, embedding=embeddings)
            retriever = vectorstore.as_retriever()
            
            contextualize_q_system_prompt = (
                    "Given a chat history and the latest user question"
                    "which might reference context in the chat history"
                    "formulate a standalone question which can be understood"
                    "without the chat history. Do NOT answer the question"
                    "just reformulate it if needed and otherwise return it as is."
            )
            
            contextualize_q_prompt = ChatPromptTemplate.from_messages(
                [
                    ('system', contextualize_q_system_prompt),
                    MessagesPlaceholder('chat_history'),
                    ('human','{input}')
                ]
            )
            
            history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)
            
            system_prompt = ( 
                "You are an assistant for question-answering tasks. "
                "Use the following pieces of retrieved context to answer "
                "the question. If you don't know the answer, say that you "
                "don't know. Use three sentences maximum and keep the "
                "answer concise."
                "\n\n"
                "{context}"
            )
            
            qa_prompt = ChatPromptTemplate.from_messages(
                [('system',system_prompt),
                MessagesPlaceholder('chat_history'),
                ('human','{input}')
                ]
            )
            
            question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
            rag_chain = create_retrieval_chain(history_aware_retriever,question_answer_chain)
            
            
            def get_session_history(session_id:str) -> BaseChatMessageHistory:
                if session_id not in st.session_state.store:
                    st.session_state.store[session_id] = ChatMessageHistory()
                return st.session_state.store[session_id]
            
            
            conversation_rag_chain = RunnableWithMessageHistory(
                rag_chain,
                get_session_history,
                input_messages_key='input',
                history_messages_key='chat_history',
                output_messages_key='answer'
            ) 
            
            user_input = st.text_input('your Question')
            if user_input:
                session_history = get_session_history(session_id)
                response = conversation_rag_chain.invoke(
                    {"input":user_input}, 
                    config={
                        'configurable':{'session_id':session_id}
                        }
                    )
                
                st.write(st.session_state.store)
                st.write("Assistant", response['answer'])
                st.write("chat_history", session_history.messages)
else:
    st.warning('Please enter the groq api key')
                
                

                    
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            