import streamlit as st
import requests
import os
from dotenv import load_dotenv
import docx

# Load API key from .env
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # Use your Groq API key

# Streamlit page config
st.set_page_config(
    page_title="Future Mind AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for gradient, buttons, and UI
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #f0f3f7, #d9e6f2);
    font-family: 'Arial', sans-serif;
}
h1, h2, h3 {
    color: #1f2937;
}
.stButton>button {
    background: linear-gradient(90deg,#4f46e5,#6366f1);
    color: white;
    border-radius: 8px;
    padding: 0.5em 1em;
    font-weight: bold;
    transition: transform 0.2s;
}
.stButton>button:hover {
    transform: scale(1.05);
}
.stTextArea>div>textarea {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.image("assets/logo.png", width=120)
st.sidebar.title("Future Mind AI")
st.sidebar.markdown("**Your AI-powered lecture assistant!**")
mode = st.sidebar.radio("Mode", ["Light", "Dark"])
if mode == "Dark":
    st.markdown('<style>body {background-color: #1f2937; color: #f3f4f6;}</style>', unsafe_allow_html=True)

# Tabs
tab1, tab2 = st.tabs(["💬 Chat with AI", "📄 Upload & Summarize Notes"])

# --- Chat Tab ---
with tab1:
    st.header("AI Chat Assistant")
    user_input = st.text_area("Ask your question here:", placeholder="Type your question...")

    if st.button("Generate Answer"):
        if user_input.strip():
            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "llama3.3-8b-8192",  # LLaMA 3.3
                "messages": [{"role": "user", "content": user_input}]
            }
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=payload
            )
            if response.status_code == 200:
                result = response.json()
                st.success(result["choices"][0]["message"]["content"])
            else:
                st.error("❌ Error connecting to Groq API")
        else:
            st.warning("⚠️ Please enter a question!")

# --- Upload & Summarize Tab ---
with tab2:
    st.header("Upload Lecture Notes")
    uploaded_file = st.file_uploader("Upload your text or Word file:", type=["txt", "docx"])

    if uploaded_file:
        try:
            # Read docx or txt
            if uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                doc = docx.Document(uploaded_file)
                file_content = "\n".join([para.text for para in doc.paragraphs])
            else:
                file_content = uploaded_file.read().decode("utf-8", errors="ignore")

            st.text_area("Preview", file_content, height=200)

            if st.button("Generate Summary"):
                headers = {
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": "llama3.3-8b-8192",
                    "messages": [{"role": "user", "content": f"Summarize this:\n{file_content}"}]
                }
                response = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers=headers,
                    json=payload
                )
                if response.status_code == 200:
                    result = response.json()
                    summary = result["choices"][0]["message"]["content"]
                    st.success("✅ Summary Generated!")
                    st.text_area("Summary", summary, height=200)
                    st.download_button(
                        label="📥 Download Summary",
                        data=summary,
                        file_name="Lecture_Summary.txt"
                    )
                else:
                    st.error("❌ Error connecting to Groq API")
        except Exception as e:
            st.error(f"Error reading file: {e}")
