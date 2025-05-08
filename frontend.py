from rag_pipeline import answer_query, llm_model
from vector_database import upload_pdf, load_pdf, create_chunks, create_vector_store, load_vector_store
import streamlit as st
import os

# Initialize session state
if 'vector_store' not in st.session_state:
    st.session_state.vector_store = load_vector_store()
if 'processed_files' not in st.session_state:
    st.session_state.processed_files = set()

# Setup Upload PDF functionality
uploaded_file = st.file_uploader("Upload PDF",
                                type="pdf",
                                accept_multiple_files=False)

# Chatbot interface
user_query = st.text_area("Enter your prompt: ", height=150, placeholder="Ask Anything!")

ask_question = st.button("Ask AI Assistant")

if ask_question:
    if uploaded_file:
        # Only process PDF if it hasn't been processed before
        if uploaded_file.name not in st.session_state.processed_files:
            with st.spinner('Processing Provided Documents...'):
                upload_pdf(uploaded_file)
                documents = load_pdf(os.path.join('pdfs', uploaded_file.name))
                text_chunks = create_chunks(documents)
                st.session_state.vector_store = create_vector_store(text_chunks)
                st.session_state.processed_files.add(uploaded_file.name)
        
        # Display user message
        st.chat_message("user").write(user_query)
        
        # Get response using RAG pipeline with progress indicator
        if st.session_state.vector_store:
            with st.spinner('Searching for answer...'):
                # Limit number of retrieved docs for faster processing
                retrieved_docs = st.session_state.vector_store.similarity_search(user_query, k=3)
                response = answer_query(documents=retrieved_docs, model=llm_model, query=user_query)
            
            # Clean up response
            if hasattr(response, 'content'):
                clean_response = response.content
            else:
                clean_response = str(response)
            
            if '<think>' in clean_response:
                clean_response = clean_response.split('</think>')[-1].strip()
            
            st.chat_message("AI Assistant").write(clean_response)
        else:
            st.error("Error: Could not process the document. Please try again.")
    else:
        st.error("Please upload a valid PDF file first!")