from rag_pipeline import answer_query, llm_model
from vector_database import upload_pdf, load_pdf, create_chunks, create_vector_store, load_vector_store
import streamlit as st
import os

# Configure the Streamlit page
st.set_page_config(
    page_title="AskAnsys Assistant",
    page_icon="ansys-logo-3-1.png",
    layout="wide"
)

# Custom CSS for Ansys branding
st.markdown("""
<style>
    /* Ansys Colors */
    :root {
        --ansys-blue: #0066A4;
        --ansys-dark-blue: #004F7C;
        --ansys-light-blue: #E5F2F9;
        --ansys-gray: #58595B;
    }
    
    /* Header styling */
    .stApp header {
        background-color: var(--ansys-blue) !important;
    }
    
    /* Main content area */
    .main {
        background-color: #FFFFFF;
    }
    
    /* Custom button styling */
    .stButton > button {
        background-color: var(--ansys-blue);
        color: white;
        border: none;
        border-radius: 4px;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    .stButton > button:hover {
        background-color: var(--ansys-dark-blue);
    }
    
    /* Chat message styling */
    .stChatMessage {
        background-color: #F0F2F6 !important;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid #E6E6E6;
    }
    
    /* User message styling */
    .stChatMessage [data-testid="StyledLinkIconContainer"] {
        background-color: var(--ansys-blue) !important;
    }
    
    /* Assistant message styling */
    .stChatMessage [data-testid="StyledLinkIconContainer"] + div {
        background-color: white !important;
        color: #333333 !important;
    }
    
    /* Message text styling */
    .stChatMessage p {
        color: #333333 !important;
    }
    
    /* File uploader styling */
    .stUploadedFile {
        border: 2px dashed var(--ansys-blue);
        border-radius: 4px;
        padding: 1rem;
    }
    
    /* Text area styling */
    .stTextArea > div > div {
        border-color: var(--ansys-blue);
    }
    
    /* Error message styling */
    .stError {
        color: #D9534F;
        border-left: 4px solid #D9534F;
    }
    
    /* Chat container styling */
    [data-testid="stChatMessageContainer"] {
        background-color: #F8F9FA;
        padding: 1rem;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Add Ansys logo and title
col1, col2 = st.columns([1, 4])
with col1:
    st.image("ansys-logo-3-1.png", width=100)
with col2:
    st.title("AskAnsys Assistant")
    st.markdown("Your intelligent guide to Ansys software and documentation")

# Initialize session state
if 'vector_store' not in st.session_state:
    st.session_state.vector_store = load_vector_store()
if 'processed_files' not in st.session_state:
    st.session_state.processed_files = set()
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'current_answer' not in st.session_state:
    st.session_state.current_answer = None

# Main content area
st.subheader("📄 Document Upload")
uploaded_file = st.file_uploader(
    "Upload Ansys documentation or guides (PDF)",
    type="pdf",
    accept_multiple_files=False,
    help="Upload Ansys user guides, documentation, or technical papers"
)

st.subheader("💬 Ask a Question")
user_query = st.text_area(
    "Enter your question about Ansys software:",
    height=100,
    placeholder="e.g., 'How do I set up a transient thermal analysis?' or 'What are the best practices for meshing in Fluent?'"
)

ask_question = st.button("Get Answer", use_container_width=True)

# Current answer section
if ask_question:
    if uploaded_file:
        # Only process PDF if it hasn't been processed before
        if uploaded_file.name not in st.session_state.processed_files:
            with st.spinner('📚 Processing Ansys documentation...'):
                upload_pdf(uploaded_file)
                documents = load_pdf(os.path.join('pdfs', uploaded_file.name))
                text_chunks = create_chunks(documents)
                st.session_state.vector_store = create_vector_store(text_chunks)
                st.session_state.processed_files.add(uploaded_file.name)
        
        # Process the query and get response
        if st.session_state.vector_store:
            with st.spinner('🔍 Searching Ansys knowledge base...'):
                retrieved_docs = st.session_state.vector_store.similarity_search(user_query, k=3)
                response = answer_query(documents=retrieved_docs, model=llm_model, query=user_query)
            
            # Clean up the response
            if hasattr(response, 'content'):
                clean_response = response.content
            else:
                clean_response = str(response)
            
            if '<think>' in clean_response:
                clean_response = clean_response.split('</think>')[-1].strip()
            
            # Store current Q&A in session state and history
            st.session_state.current_answer = {
                "question": user_query,
                "answer": clean_response
            }
            st.session_state.chat_history.append({"role": "user", "content": user_query})
            st.session_state.chat_history.append({"role": "assistant", "content": clean_response})
        else:
            st.error("⚠️ Error: Could not process the document. Please try again.")
    else:
        st.warning("📋 Please upload an Ansys documentation file (PDF) first!")

# Display current answer if exists
if st.session_state.current_answer:
    st.subheader("Current Answer")
    with st.container():
        st.info("Question: " + st.session_state.current_answer["question"])
        st.success("Answer: " + st.session_state.current_answer["answer"])

# Separator
st.markdown("---")

# Chat history at the bottom
with st.expander("📜 Conversation History", expanded=False):
    for message in reversed(st.session_state.chat_history):
        if message["role"] == "user":
            st.chat_message("user", avatar="👤").write(message["content"])
        else:
            st.chat_message("assistant", avatar="🔧").write(message["content"])

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: var(--ansys-gray);'>
    <p>AskAnsys Assistant v1.0 | Need help? Contact: support@ansys.com</p>
</div>
""", unsafe_allow_html=True)