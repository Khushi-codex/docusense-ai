import streamlit as st
from groq import Groq
import numpy as np
from pypdf import PdfReader
import re

st.set_page_config(page_title="DocuSense AI", page_icon="📄", layout="wide")
st.title("💼 DocuSense AI – Regional Multi-Document Assistant")
st.write("Upload any research paper, report, or resume. Get lightning-fast structural insights in English, Hindi, or Hinglish.")

# Initialize Groq Client safely
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("🔑 Missing GROQ_API_KEY in Streamlit Secrets!")

# File uploader
uploaded_file = st.file_uploader("Upload Document (.pdf, .txt):", type=["pdf", "txt"])

# Simple, ultra-fast vector search system built directly in python (No heavy installations needed)
def clean_and_split_text(text, chunk_size=800):
    text = re.sub(r'\s+', ' ', text) # Clean messy PDF whitespaces
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        if len(chunk.strip()) > 10:
            chunks.append(chunk)
    return chunks

def keyword_relevance_score(chunk, query):
    """Calculates rapid relevance matching to simulate an embedding search instantly."""
    query_words = set(query.lower().split())
    chunk_words = chunk.lower()
    score = sum(1 for word in query_words if word in chunk_words)
    return score

if uploaded_file is not None:
    # Read text using clean buffering
    with st.spinner("Parsing document structure layout..."):
        file_type = uploaded_file.name.split(".")[-1].lower()
        document_text = ""
        
        if file_type == "pdf":
            reader = PdfReader(uploaded_file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    document_text += page_text + "\n"
        else:
            document_text = uploaded_file.read().decode("utf-8")

    if document_text.strip():
        st.success(f"✅ {uploaded_file.name} successfully indexed into local knowledge database!")
        
        # Prepare text database chunks
        document_chunks = clean_and_split_text(document_text)
        
        user_input = st.text_input("Ask anything about this document:", placeholder="e.g., Explain the core methodology or summarize in 5 key bullet points.")
        
        if st.button("Query Knowledge Base") or user_input:
            if user_input.strip():
                with st.spinner("Querying vector index & generating localized response..."):
                    # Find the top relevant text chunks matching the user's specific query
                    scored_chunks = [(chunk, keyword_relevance_score(chunk, user_input)) for chunk in document_chunks]
                    scored_chunks.sort(key=lambda x: x[1], reverse=True)
                    
                    # Pull only the top 3 highly relevant context paragraphs (Guarantees no 413 Token Limit crash)
                    top_context = "\n\n".join([item[0] for item in scored_chunks[:3]])
                    
                    system_rules = (
                        "You are DocuSense AI, a professional, senior technical recruiter and research mentor built for students and businesses in India. "
                        "Analyze the provided context snippet carefully to answer the user's question. "
                        "STRICT LANGUAGE LOCALIZATION POLICY:\n"
                        "1. If the user asks or interacts in professional English, respond in clean, formal corporate English.\n"
                        "2. If the user asks in Hindi, Hinglish, or conversational terms, immediately adapt. Break down complex engineering and academic jargons into very friendly, easy-to-understand local Indian examples (using analogies like local markets, colleges, cricket, or daily life). Do not use slang like 'bhai', keep it highly respectable but culturally warm."
                    )
                    
                    prompt = f"Context from Document:\n{top_context}\n\nUser Question: {user_input}\n\nAnswer the question perfectly using the context above:"
                    
                    try:
                        completion = client.chat.completions.create(
                            model="qwen/qwen3.8-27b",
                            messages=[
                                {"role": "system", "content": system_rules},
                                {"role": "user", "content": prompt}
                            ],
                            temperature=0.3
                        )
                        
                        st.subheader("🤖 DocuSense AI Analysis:")
                        st.write(completion.choices[0].message.content)
                        
                    except Exception as e:
                        st.error(f"Engine Timeout or Connection Error: {e}")
            else:
                st.warning("Please type a valid question to query the document.")

