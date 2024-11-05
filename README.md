# Open-Source Model ChatBot Suite with Streamlit

Welcome to the **Open-Source Model ChatBot Suite**! This project leverages open-source language models and the LangChain library, providing an easy-to-use interface built with Streamlit for interacting with various chatbot functionalities. With an emphasis on flexibility and adaptability, this suite allows users to experiment with different chatbot models and use cases, making it a valuable tool for developers, researchers, and hobbyists alike. 🚀

## Features

### 💬 1. Q&A ChatBot
A straightforward Q&A chatbot where users can select from various open-source models to engage in real-time conversation. This basic chatbot functionality provides a fresh session each time, ensuring that no chat history is stored between sessions, which is ideal for quick, isolated interactions with different models.

### 📄 2. RAG Document Q&A
In this setup, the chatbot leverages **Retrieval-Augmented Generation (RAG)** to answer questions based on the content of pre-uploaded documents. Users can ask questions related to specific research papers, such as PDF files on topics like attention mechanisms or language models, making it perfect for focused, document-specific insights.

### 🗃️ 3. RAG Q&A with Conversational Memory
This advanced chatbot goes a step further by allowing users to upload one or more PDF files and conduct a multi-turn conversation based on the content. With session-based memory, this chatbot retains the context of previous questions within the session, making it more interactive and providing continuity throughout the conversation. Ideal for exploring detailed content across multiple files while keeping track of the dialogue history.

## Future Enhancements
Stay tuned! 🎉 Additional chatbot functionalities are on the way to make this project even more versatile and user-friendly.

## Getting Started

1. **Install Requirements**  
   Ensure all dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the App**  
   To launch any chatbot, navigate to the relevant folder and run:
   ```bash
   streamlit run app.py
   ```
   This will start a local Streamlit server, and the app can be accessed via your browser.

3. **Choose Your Chatbot**  
   Each chatbot is designed for different use cases, so feel free to explore each one based on your needs:
   - **Q&A ChatBot**: Simple Q&A without memory.
   - **RAG Document Q&A**: Q&A based on pre-loaded PDFs.
   - **RAG Q&A with Memory**: Upload files and enjoy conversation with session-based memory.

Enjoy exploring, experimenting, and extending this open-source chatbot suite! 🌐