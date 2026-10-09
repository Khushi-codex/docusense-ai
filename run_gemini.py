import streamlit as st
from groq import Groq  # <-- Upgraded engine library
from pypdf import PdfReader

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

if submit_button:
    if extracted_text or user_input:
        with st.spinner("Analyzing document with high-speed engine..."):
            try:
                # Initialize the Groq client with your new key
                client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                
                system_rules = (
                    "You are a professional, senior technical recruiter and document expert built for engineering students in India. "
                    "Meticulously analyze the provided document context. "
                    "Strictly follow the user's language choice: If the user asks a question in professional English, reply in clean, corporate English. "
                    "If the user asks in Hindi or Hinglish, explain the concepts in a friendly, easy-to-understand local manner. "
                    "Maintain a helpful, highly polished, and professional tone at all times. Do not use overly casual slang like 'bhai'."
                )
                        
                
                final_prompt = f"Context Document:\n{extracted_text}\n\nUser Question: {user_input}"
                
                # Change the model argument on line 45 to this:
                completion = client.chat.completions.create(
                    model="qwen/qwen3.8-27b",  # <-- Updated active model name
                    messages=[
                        {"role": "system", "content": system_rules},
                        {"role": "user", "content": final_prompt}
                    ],
                )

                
                st.success("🤖 AI Analysis Result:")
                st.write(completion.choices[0].message.content)
                
            except Exception as e:
                st.error(f"Engine connection issue: {e}")
    else:
        st.warning("Please upload a file or type a question!")
