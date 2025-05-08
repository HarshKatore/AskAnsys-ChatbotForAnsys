from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Step 1: Setup LLM (Use DeepSeek R1 with Groq)
llm_model = ChatGroq(
    model="deepseek-r1-distill-llama-70b",
    temperature=0.3,  # Lower temperature for faster, more focused responses
    max_tokens=500  # Limit response length for faster generation
)

# Step 2: Helper functions for document handling
def get_context(documents):
    # Limit context length for faster processing
    max_context_length = 2000
    context = "\n\n".join([doc.page_content for doc in documents])
    return context[:max_context_length]

# Step 3: Setup prompt template with more focused instructions
custom_prompt_template = ChatPromptTemplate.from_template("""
Answer the question concisely using only the information in the context.
If the answer isn't in the context, just say "I don't have enough information to answer that."
Question: {question} 
Context: {context} 
Answer:
""")

# Step 4: Create optimized answer function
def answer_query(documents, model, query):
    context = get_context(documents)
    chain = custom_prompt_template | model | StrOutputParser()
    return chain.invoke({"question": query, "context": context})