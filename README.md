
# 📚 Research Paper Chatbot with Streamlit and Ollama

This project provides a web-based chatbot that allows you to upload research papers (in PDF format) and ask questions about their content. It runs entirely on your local machine, ensuring your data remains private.

The application uses a Retrieval-Augmented Generation (RAG) pipeline powered by LangChain, Ollama, and ChromaDB.

## Features

* **Local & Private**: All processing happens on your machine. No data is sent to external APIs.
* **Multiple Document Support**: Upload and query multiple PDFs simultaneously.
* **Source Citing**: The chatbot's answers are supported by snippets from the source documents.
* **Swappable LLMs**: Easily switch between different local models supported by Ollama (e.g., Llama 3, Mistral, CodeLlama).
* **User-Friendly Interface**: Simple and intuitive UI built with Streamlit.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

1. **Python 3.9+**: [Download Python](https://www.python.org/downloads/)
2. **Ollama**: You must have Ollama installed and running. [Download Ollama](https://ollama.com/).

---

## Setup and Installation (Manual)

**1. Install Ollama and Pull a Model**

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

```bash
# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate
```

**4. Install Python Dependencies**

```bash
pip install -r requirements.txt
```

---

## Run the Application (Manual)

With your virtual environment activated and Ollama running in the background, start the Streamlit app:

```bash
streamlit run app.py
```

Your browser should open the app at `http://localhost:8501`.

---

## Run with Docker (Recommended)

You can also run the chatbot inside a Docker container. The image includes all dependencies (Streamlit, LangChain, ChromaDB, and Ollama with `llama3`).

### CPU Version

```bash
sudo docker run -p 8501:8501 -p 11434:11434 --name chatbot ghcr.io/pip700/chatbot:lamma3
```

### GPU Version (NVIDIA CUDA)

If you have a supported NVIDIA GPU and CUDA installed:

```bash
sudo docker run --gpus all -p 8501:8501 -p 11434:11434 --name chatbot ghcr.io/pip700/chatbot:lamma3
```

Once running, open your browser at:

```
http://localhost:8501
```

> ℹ️ The chatbot API (Ollama service) will be available at `http://localhost:11434`.

---

## How to Use the Chatbot

1. **Select a Model** in the sidebar.
2. **Upload PDFs** using the drag-and-drop uploader.
3. **Process Documents** to build embeddings and store them in a local vector DB.
4. **Ask Questions** in the chat box.
5. **View Sources** with supporting text snippets.
6. **Clear Data** anytime to reset chat history and the vector store.

---

## Project Structure

```
research-paper-chatbot/
├── utils/
│   ├── __init__.py
│   ├── pdf_processor.py    # Handles PDF text extraction
│   └── vector_store.py     # Manages the ChromaDB vector store
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

