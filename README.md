# DocuSense AI – Multi-Format Regional Document Assistant 🚀

An interactive, production-ready web application built to parse structural text from multiple document formats and deliver context-aware, localized intelligence using advanced Large Language Models (LLMs). 

Developed explicitly to solve a real-world problem for small business owners and engineering students in India by breaking down complex English documentation into clear corporate English, Hindi, or conversational Hinglish based on user preference.

🔗 **Live Application Link:** https://docusense-ai-hhh8klvbfuezfcdwxk9be8.streamlit.app/

---

## 🌟 Key Features

- **Smart Text Chunking**: Custom algorithm breaks down extensive documents into optimal token segments, entirely bypassing the 7,000 ITPM limit.
- **Universal Processing**: Seamlessly parses multi-page PDFs using `pypdf`.
- **Dual-Language Intelligent Response**: Senior Recruiter persona supporting both professional English and local Hinglish/Hindi explanations.
- **High-Performance LLM**: Powered by the fast `qwen/qwen3.8-27b` architecture hosted on Groq.
---

## 🛠️ Tech Stack & Architecture

- **Frontend Interface:** Streamlit (State-Driven Python Web Framework)
- **AI Processing Backend:** Groq Cloud Developer Client Engine SDK
- **Language Inference Model:** Qwen 3.8 LLM Framework Layer
- **Structural Text Extraction:** PyPDF (Document Object Parsing Pipeline)
- **Version Control & CI/CD:** Git & Streamlit Community Cloud Ecosystem

---

## 📁 Repository Structure

```text
├── .streamlit/
│   └── secrets.toml      # Hidden local environment parameters (Excluded from Git)
├── run_gemini.py         # Main execution file handling Frontend UI, State, & API routing
├── requirements.txt      # Automated dependency manifest for remote cloud containers
└── README.md             # Project documentation and architectural review
```

---

## 🚀 Local Installation & Configuration

To download, configure, and execute this application locally on your workstation, follow these setup directives:

### 1. Clone the Repository
```bash
git clone https://github.com
cd docusense-ai
```

### 2. Install Package Dependencies
Ensure your environment is running Python 3.10+ and execute:
```bash
pip install -r requirements.txt
```

### 3. Establish Secure Access Vault
Create a configuration folder and file structure to hold your API keys securely outside the root logic:
```bash
mkdir .streamlit
```
Inside the `.streamlit/` folder, create a file named `secrets.toml` and input your developer key:
```toml
GROQ_API_KEY = "gsk_your_private_groq_api_credential_string"
```

### 4. Execute the Application Instance
Launch the reactive Streamlit application layer locally:
```bash
streamlit run run_gemini.py
```
Your local system will initialize a web hosting container and automatically open the interactive panel interface inside your default browser at `http://localhost:8501`.
