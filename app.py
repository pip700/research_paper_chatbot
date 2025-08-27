import streamlit as st
import tempfile
import os
from pathlib import Path
from utils.pdf_processor import extract_text_from_pdf, create_text_splitter
from utils.vector_store import initialize_vector_store, add_texts_to_store
from langchain.llms import Ollama
from langchain.chains import RetrievalQA

# Page configuration
st.set_page_config(
    page_title="Research Paper Chatbot",
    page_icon="📚",
    layout="wide"
)

# Initialize session state
def initialize_session_state():
    if 'vector_store' not in st.session_state:
        st.session_state.vector_store = initialize_vector_store()
    if 'qa_chain' not in st.session_state:
        llm = Ollama(model="llama3", temperature=0.1)
        st.session_state.qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=st.session_state.vector_store.as_retriever(search_kwargs={"k": 4}),
            return_source_documents=True
        )
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'processed_files' not in st.session_state:
        st.session_state.processed_files = set()

initialize_session_state()

# Sidebar
st.sidebar.title("⚙️ Settings")
st.sidebar.header("Model Configuration")

# Model selection
model_name = st.sidebar.selectbox(
    "Select LLM Model",
    ["llama3", "mistral", "llama2", "codellama"],
    index=0
)

# Update the LLM in the QA chain if the model selection changes
if 'llm_model' not in st.session_state or st.session_state.llm_model != model_name:
    st.session_state.llm_model = model_name
    llm = Ollama(model=model_name, temperature=0.1)
    st.session_state.qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=st.session_state.vector_store.as_retriever(search_kwargs={"k": 4}),
        return_source_documents=True
    )
    st.sidebar.success(f"Switched to {model_name} model")


# File upload section
st.sidebar.header("📄 Document Processing")
uploaded_files = st.sidebar.file_uploader(
    "Upload Research Papers (PDF)",
    type="pdf",
    accept_multiple_files=True
)

def process_documents(files):
    """Process uploaded PDF documents"""
    with st.spinner("Processing documents..."):
        all_chunks = []
        for uploaded_file in files:
            if uploaded_file.name in st.session_state.processed_files:
                continue

            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_file_path = tmp_file.name

                text = extract_text_from_pdf(tmp_file_path)
                text_splitter = create_text_splitter()
                chunks = text_splitter.split_text(text)
                all_chunks.extend(chunks)
                st.session_state.processed_files.add(uploaded_file.name)

            finally:
                if 'tmp_file_path' in locals() and os.path.exists(tmp_file_path):
                    os.unlink(tmp_file_path)

        if all_chunks:
            add_texts_to_store(st.session_state.vector_store, all_chunks)
            st.sidebar.success(f"Processed {len(files)} new documents!")
        else:
            st.sidebar.info("No new documents to process.")


if uploaded_files:
    if st.sidebar.button("Process Documents"):
        process_documents(uploaded_files)

# Clear data button
if st.sidebar.button("🗑️ Clear All Data"):
    st.session_state.processed_files.clear()
    st.session_state.messages.clear()
    # Re-initialize the vector store (clearing the old one)
    st.session_state.vector_store = initialize_vector_store(clear=True)
    # Re-create the QA chain with the fresh vector store
    llm = Ollama(model=st.session_state.llm_model, temperature=0.1)
    st.session_state.qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=st.session_state.vector_store.as_retriever(search_kwargs={"k": 4}),
        return_source_documents=True
    )
    st.rerun()


# Main interface
st.title("📚 Research Paper Chatbot")
st.markdown("Ask questions about your uploaded research papers using local AI.")

# Display processed files
if st.session_state.processed_files:
    st.sidebar.subheader("Processed Files")
    for file in st.session_state.processed_files:
        st.sidebar.write(f"• {file}")

# Chat interface
st.header("💬 Chat with Your Research")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message and message["sources"]:
            with st.expander("View Sources"):
                for i, source in enumerate(message["sources"]):
                    st.write(f"**Source {i+1}**")
                    st.info(f"{source[:300]}...")

# Question input
if prompt := st.chat_input("What would you like to know about the research?"):
    if not st.session_state.processed_files:
        st.warning("Please upload and process at least one PDF document before asking questions.")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Analyzing research..."):
                try:
                    result = st.session_state.qa_chain({"query": prompt})
                    response = result["result"]
                    source_docs = result.get("source_documents", [])

                    st.markdown(response)

                    # Extract source content
                    sources = [doc.page_content for doc in source_docs] if source_docs else []

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response,
                        "sources": sources
                    })
                    # Rerun to display the sources in the expander immediately
                    st.rerun()

                except Exception as e:
                    error_msg = f"Error generating response: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })

# Instructions section
with st.expander("ℹ️ How to use this chatbot"):
    st.markdown("""
    1. **Install & Run Ollama**: Make sure the Ollama application is running on your machine.
    2. **Select LLM Model**: Choose your preferred local model from the sidebar dropdown.
    3. **Upload PDFs**: Use the sidebar to upload your research papers.
    4. **Process Documents**: Click 'Process Documents' to make them searchable.
    5. **Ask Questions**: Type your questions in the chat input below.

    **Features**:
    - Local processing (no data leaves your machine).
    - Support for multiple research papers.
    - Source citation for answers.
    - Multiple LLM model options via Ollama.
    """)
