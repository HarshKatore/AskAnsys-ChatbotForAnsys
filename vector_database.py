from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
import os

# Step 1: Upload & Load raw PDF(s)
pdfs_directory = 'pdfs/'
if not os.path.exists(pdfs_directory):
    os.makedirs(pdfs_directory)

def upload_pdf(file):
    with open(pdfs_directory + file.name, "wb") as f:
        f.write(file.getbuffer())

def load_pdf(file_path):
    loader = PDFPlumberLoader(file_path)
    documents = loader.load()
    return documents

# Step 2: Create Chunks
def create_chunks(documents): 
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 500,  # Reduced from 1000 for faster processing
        chunk_overlap = 50,  # Reduced from 200 for faster processing
        add_start_index = True
    )
    text_chunks = text_splitter.split_documents(documents)
    return text_chunks

# Step 3: Setup Embeddings Model with explicit Ollama connection
ollama_model_name = "deepseek-r1:7b"
def get_embedding_model(model_name):
    embeddings = OllamaEmbeddings(
        model=model_name,
        base_url="http://localhost:11434"  # Default Ollama URL
    )
    return embeddings

# Step 4: Vector Store Setup
FAISS_DB_PATH = "vectorstore/db_faiss"

def create_vector_store(text_chunks, model_name=ollama_model_name):
    try:
        embeddings = get_embedding_model(model_name)
        faiss_db = FAISS.from_documents(text_chunks, embeddings)
        faiss_db.save_local(FAISS_DB_PATH)
        return faiss_db
    except Exception as e:
        print(f"Error connecting to Ollama: {e}")
        print("Please ensure Ollama is running with: 'ollama serve' command")
        raise

def load_vector_store():
    try:
        if os.path.exists(FAISS_DB_PATH):
            embeddings = get_embedding_model(ollama_model_name)
            return FAISS.load_local(
                FAISS_DB_PATH, 
                embeddings,
                allow_dangerous_deserialization=True  # Only enable this since we're loading our own files
            )
        return None
    except Exception as e:
        print(f"Error loading vector store: {e}")
        return None