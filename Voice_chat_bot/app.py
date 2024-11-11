from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from audio_recorder_streamlit import audio_recorder
import streamlit as st
import os
import whisper
import tempfile
from gtts import gTTS
import io
from langchain_groq import ChatGroq

st.set_page_config(page_title="Llamma Voice & Chat Bot", page_icon="🦙")
st.title("Llamma Voice & Chat Bot 🦙")

def llm_selector():
    models=["llama3-groq-8b-8192-tool-use-preview", "gemma2-9b-it", 'llama-3.2-3b-preview']
    with st.sidebar:
        return st.selectbox("Model", models)

# Set up memory
msgs = StreamlitChatMessageHistory(key="langchain_messages")
if len(msgs.messages) == 0:
    msgs.add_ai_message("How can I help you?")


# Set up the LangChain, passing in Message History
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an AI chatbot having a conversation with a human."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ]
)

chain = prompt | ChatGroq(model=llm_selector(), api_key='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')  #Ollama( model=llm_selector(), temperature=0)
chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: msgs,
    input_messages_key="question",
    history_messages_key="history",
)

# Function to transcribe audio
@st.cache_resource
def load_whisper_model(model_size):
    return whisper.load_model(model_size)

def transcribe_audio(audio_file):

    # Options for the transcribe model ["base", "tiny", "small", "medium", "large"]
    model = load_whisper_model("base")
    result = model.transcribe(audio_file, fp16=False)
    return result["text"]

# Function for text-to-speech
def text_to_speech(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    mp3_fp = io.BytesIO()
    tts.write_to_fp(mp3_fp)
    return mp3_fp.getvalue()


# Get LLM response
def get_llm_response(input: str) -> str:

    # Note: new messages are saved to history automatically by Langchain during run
    config = {"configurable": {"session_id": "any"}}
    response = chain_with_history.invoke({"question": input}, config)

    return response


# Render current messages from StreamlitChatMessageHistory
for msg in msgs.messages:
    st.chat_message(msg.type).write(msg.content)

with st.sidebar:
    audio_bytes = audio_recorder(pause_threshold=1.0, sample_rate=16_000)

# If user inputs a new prompt, generate and draw a new response
if prompt := st.chat_input():
    st.chat_message("human").write(prompt)
    msgs.add_user_message(prompt)
    audio_bytes = None

if file:= st.sidebar.file_uploader('Upload audio file'):
    with st.spinner("Transcribing..."):
        # Use tempfile to save and handle the file if Whisper expects a file path
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            temp_audio.write(file.read())  # Write the uploaded file to temp file
            temp_audio_path = temp_audio.name  # Get temp file path

        # Now pass the temp file path to transcribe_audio
        transcription = transcribe_audio(temp_audio_path)
        
        if transcription:
            st.chat_message("human").write(transcription)
            msgs.add_user_message(transcription)

        # Clean up
        os.unlink(temp_audio_path)  # Delete the temp file after use

    
# If audio bytes are available, transcribe and add to chat history
if audio_bytes is not None:

    # Save the recorded audio to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(audio_bytes)
        temp_audio_path = temp_audio.name

    with st.spinner("Transcribing..."):
        transcription = transcribe_audio(temp_audio_path)
        if transcription:
            st.chat_message("human").write(transcription)
            msgs.add_user_message(transcription)

    # Clean up
    os.unlink(temp_audio_path)

# If last message is not from the AI, generate a new response
if st.session_state.langchain_messages[-1].type != "ai":
    with st.chat_message("ai"):
        #st.write(st.session_state.langchain_messages[-1].content)
        with st.spinner("Thinking🤔..."):
            response = get_llm_response(st.session_state.langchain_messages[-1].content)
        
        print("="*100)
        print('SESSION STATE :',st.session_state)
        print("="*100)
        
        st.write(response.content)
        with st.spinner("Generating audio response..."):
            tts_audio = text_to_speech(response.content)
            # auto-play audio
            st.audio(tts_audio, format="audio/mpeg", autoplay=True)

