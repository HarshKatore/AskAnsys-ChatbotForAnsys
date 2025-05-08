from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Step 1: Setup LLM (Use DeepSeek R1 with Groq)
llm_model = ChatGroq(model="deepseek-r1-distill-llama-70b")

# Step 2: Helper functions for document handling
def get_context(documents):
    context = "\n\n".join([doc.page_content for doc in documents])
    return context

# Step 3: Setup prompt template
custom_prompt_template = ChatPromptTemplate.from_template("""
Use the pieces of information provided in the context to answer user's question.
If you dont know the answer, just say that you dont know, dont try to make up an answer. 
Dont provide anything out of the given context
Question: {question} 
Context: {context} 
Answer:
""")

def answer_query(documents, model, query):
    context = get_context(documents)
    chain = custom_prompt_template | model
    return chain.invoke({"question": query, "context": context})