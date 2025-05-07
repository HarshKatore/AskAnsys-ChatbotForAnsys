from rag_pipeline import answer_query, retrieve_docs, llm_model
import streamlit as st

# Configure Ansys theme and page settings
st.set_page_config(
    page_title="AskAnsys - Your Engineering Assistant",
    page_icon="🔧",
    layout="wide"
)

# Custom CSS for Ansys styling
st.markdown("""
    <style>
    .stApp {
        background-color: #f8f9fa;
    }
    .main {
        padding: 2rem;
    }
    .st-emotion-cache-1c7y2kd {
        background-color: #0066A1;  /* Ansys Blue */
        color: white;
        border: none;
        padding: 0.5rem 1rem;
    }
    .st-emotion-cache-1c7y2kd:hover {
        background-color: #004d7a;
    }
    .st-emotion-cache-16idsys {
        border-color: #0066A1;
    }
    .st-bw {
        color: #333333;  /* Ansys Dark Gray */
    }
    </style>
""", unsafe_allow_html=True)

# Header with Ansys branding
st.markdown("""
    <div style='text-align: center; padding: 2rem;'>
        <h1 style='color: #0066A1; margin-bottom: 0;'>AskAnsys</h1>
        <p style='color: #666666; font-size: 1.2em;'>Your Engineering Simulation Assistant</p>
    </div>
""", unsafe_allow_html=True)

# Create columns for better layout
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### Upload Engineering Documentation")
    uploaded_file = st.file_uploader(
        "Upload your Ansys documentation (PDF)",
        type="pdf",
        accept_multiple_files=False,
        help="Upload Ansys manuals, guides, or documentation in PDF format"
    )

st.markdown("---")

# Chat interface
st.markdown("### Engineering Query Interface")
user_query = st.text_area(
    "What would you like to know about Ansys?",
    height=100,
    placeholder="Ask about Ansys simulations, setup, analysis, or any engineering queries..."
)

# Center the button
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    ask_question = st.button("Ask AskAnsys", use_container_width=True)

if ask_question:
    if uploaded_file and user_query:
        st.markdown("---")
        # User message
        st.chat_message("user", avatar="👤").write(user_query)
        
        # RAG Pipeline
        retrieved_docs=retrieve_docs(user_query)
        response=answer_query(documents=retrieved_docs, model=llm_model, query=user_query)
        
        # Assistant message with Ansys branding
        st.chat_message("assistant", avatar="🔧").write(response)
    
    elif not uploaded_file:
        st.error("📚 Please upload an Ansys documentation file (PDF) first!")
    else:
        st.error("❓ Please enter your engineering query!")