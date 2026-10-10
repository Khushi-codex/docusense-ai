import streamlit as st
from groq import Groq
from pypdf import PdfReader
import concurrent.futures  # <-- Added for high-speed parallel processing

st.set_page_config(page_title="AI Document Assistant", page_icon="📄")
st.title("💼 AI Multi-Document Assistant")
st.write("Upload a PDF or a TXT document and get instant feedback.")

uploaded_file = st.file_uploader("Upload a document (.pdf or .txt):", type=["pdf", "txt"])

extracted_text = ""
if uploaded_file is not None:
    try:
        file_details = uploaded_file.name.split(".")[-1].lower()
        if file_details == "pdf":
            reader = PdfReader(uploaded_file)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    extracted_text += text + "\n"
            st.success("PDF uploaded and parsed successfully!")
        elif file_details == "txt":
            extracted_text = uploaded_file.read().decode("utf-8")
            st.success("TXT file uploaded and read successfully!")
    except Exception as e:
        st.error(f"Error reading file: {e}")

user_input = st.text_input("Ask a question about the document:", placeholder="e.g., Is this resume good for off-campus?")
submit_button = st.button("Analyze Document")

def split_text_into_chunks(text, max_chars=12000):
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0
    
    for word in words:
        if current_length + len(word) + 1 > max_chars:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
            current_length = len(word)
        else:
            current_chunk.append(word)
            current_length += len(word) + 1
            
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks

# --- HELPER FUNCTION FOR A SINGLE API CALL ---
def process_single_chunk(client, chunk, idx, total_chunks, system_rules, user_input):
    chunk_prompt = f"Context Document (Part {idx+1}/{total_chunks}):\n{chunk}\n\nUser Question: {user_input}"
    try:
        completion = client.chat.completions.create(
            model="qwen/qwen3.8-27b",
            messages=[
                {"role": "system", "content": system_rules},
                {"role": "user", "content": chunk_prompt}
            ],
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"[Error processing section {idx+1}: {e}]"

if submit_button:
    if extracted_text or user_input:
        with st.spinner("Analyzing all document sections simultaneously..."):
            try:
                client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                
                system_rules = (
                    "You are a professional, senior technical recruiter and document expert built for engineering students in India. "
                    "Meticulously analyze the provided document context. "
                    "Strictly follow the user's language choice: If the user asks a question in professional English, reply in clean, corporate English. "
                    "If the user asks in Hindi or Hinglish, explain the concepts in a friendly, easy-to-understand local manner. "
                    "Maintain a helpful, highly polished, and professional tone at all times. Do not use overly casual slang like 'bhai'."
                )
                
                text_chunks = split_text_into_chunks(extracted_text)
                
                # --- FAST PARALLEL EXECUTION ---
                # This executes all chunks at the exact same time instead of waiting in line
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    futures = [
                        executor.submit(process_single_chunk, client, chunk, idx, len(text_chunks), system_rules, user_input)
                        for idx, chunk in enumerate(text_chunks)
                    ]
                    chunk_replies = [future.result() for future in futures]
                
                # Synthesize the partial answers into a unified final answer
                synthesis_prompt = (
                    f"The user asked: '{user_input}'\n\n"
                    f"Here are the combined notes retrieved from different parts of their document:\n"
                    f"{' '.join(chunk_replies)}\n\n"
                    f"Please provide the final combined clean response answering the user's question directly. "
                    f"If they requested a specific structure (like 5 bullet points with key details), adhere to it perfectly."
                )
                
                final_completion = client.chat.completions.create(
                    model="qwen/qwen3.8-27b",
                    messages=[
                        {"role": "system", "content": system_rules},
                        {"role": "user", "content": synthesis_prompt}
                    ],
                )
                
                st.success("🤖 AI Analysis Result:")
                st.write(final_completion.choices[0].message.content)
                
            except Exception as e:
                st.error(f"Engine connection issue: {e}")
    else:
        st.warning("Please upload a file or type a question!")
