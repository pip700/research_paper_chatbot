FROM python:3.9-slim

# Install system dependencies for sentence-transformers and Ollama
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    gcc \
    g++ \
    make \
    cmake \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Set up Python environment
WORKDIR /app
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create directory for ChromaDB
RUN mkdir -p chroma_db

# Copy application code
COPY . .

# Pre-install Llama3 model
RUN ollama serve & \
    sleep 15 && \
    ollama pull llama3 && \
    pkill ollama

# Expose ports
EXPOSE 8501 11434

# Start services
CMD sh -c "ollama serve & sleep 5 && streamlit run app.py --server.port=8501 --server.address=0.0.0.0"
