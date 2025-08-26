# 📚 Research Paper Chatbot with Streamlit and Ollama

This project provides a web-based chatbot that allows you to upload research papers (in PDF format) and ask questions about their content. It runs entirely on your local machine, ensuring your data remains private.

The application uses a Retrieval-Augmented Generation (RAG) pipeline powered by LangChain, Ollama, and ChromaDB.

## Features

-   **Local & Private**: All processing happens on your machine. No data is sent to external APIs.
-   **Multiple Document Support**: Upload and query multiple PDFs simultaneously.
-   **Source Citing**: The chatbot's answers are supported by snippets from the source documents.
-   **Swappable LLMs**: Easily switch between different local models supported by Ollama (e.g., Llama 3, Mistral, CodeLlama).
-   **User-Friendly Interface**: Simple and intuitive UI built with Streamlit.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

1.  **Python 3.9+**: [Download Python](https://www.python.org/downloads/)
2.  **Ollama**: You must have Ollama installed and running. [Download Ollama](https://ollama.com/).

## Setup and Installation

**1. Install Ollama and Pull a Model**

First, make sure the Ollama application is running. Then, pull a model from the command line. We recommend starting with `llama3`.

```bash
ollama pull llama3
```

You can also pull other models like `mistral` or `codellama`.

**2. Clone the Repository**

```bash
git clone <repository_url>
cd research-paper-chatbot
```

**3. Create a Virtual Environment**

It's highly recommended to use a virtual environment to manage dependencies.

```bash
# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate
```

**4. Install Python Dependencies**

Install all the required packages from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

This will download all necessary libraries, including Streamlit, LangChain, and the embedding models. The initial download might take a few minutes.

## How to Run the Application

With your virtual environment activated and Ollama running in the background, start the Streamlit app:

```bash
streamlit run app.py
```

Your web browser should open a new tab with the application running at `http://localhost:8501`.

## How to Use the Chatbot

1.  **Select a Model**: Use the sidebar to choose which Ollama model you want to use.
2.  **Upload PDFs**: Drag and drop your research papers into the file uploader in the sidebar.
3.  **Process Documents**: Click the "Process Documents" button. The app will extract text, create embeddings, and store them in a local vector database.
4.  **Ask Questions**: Once processing is complete, type your questions into the chat input box and press Enter.
5.  **View Sources**: The assistant's answers will include an expandable "View Sources" section, showing the text chunks used to generate the response.
6.  **Clear Data**: If you want to start fresh with new documents, click the "Clear All Data" button to reset the vector store and chat history.

## Project Structure

```
research-paper-chatbot/
├── utils/
│   ├── __init__.py
│   ├── pdf_processor.py    # Handles PDF text extraction
│   └── vector_store.py     # Manages the ChromaDB vector store
├── app.py                  # Main Streamlit application
└── requirements.txt        # Python dependencies
└── README.md               # This file
```
