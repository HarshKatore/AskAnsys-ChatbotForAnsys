from rag_pipeline import answer_query, llm_model
from vector_database import upload_pdf, load_pdf, create_chunks, create_vector_store, load_vector_store
import streamlit as st
import os

# Initialize session state for vector store
if 'vector_store' not in st.session_state:
    st.session_state.vector_store = load_vector_store()

# Setup Upload PDF functionality
uploaded_file = st.file_uploader("Upload PDF",
                                type="pdf",
                                accept_multiple_files=False)

# Chatbot interface
user_query = st.text_area("Enter your prompt: ", height=150, placeholder="Ask Anything!")

ask_question = st.button("Ask AI Assistant")

if ask_question:
    if uploaded_file:
        # Process PDF and update vector store if needed
        upload_pdf(uploaded_file)
        documents = load_pdf(os.path.join('pdfs', uploaded_file.name))
        text_chunks = create_chunks(documents)
        st.session_state.vector_store = create_vector_store(text_chunks)
        
        # Display user message
        st.chat_message("user").write(user_query)
        
        # Get response using RAG pipeline
        if st.session_state.vector_store:
            retrieved_docs = st.session_state.vector_store.similarity_search(user_query)
            response = answer_query(documents=retrieved_docs, model=llm_model, query=user_query)
            
            # Clean up the response to show only the main content
            if hasattr(response, 'content'):
                clean_response = response.content
            else:
                clean_response = str(response)
            
            # Remove thinking process and metadata if present
            if '<think>' in clean_response:
                clean_response = clean_response.split('</think>')[-1].strip()
            
            st.chat_message("AI Assistant").write(clean_response)
        else:
            st.error("Error: Could not process the document. Please try again.")
    else:
        st.error("Please upload a valid PDF file first!")