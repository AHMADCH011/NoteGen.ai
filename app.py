import streamlit as st
import requests
import os

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="NoteGen AI",
    page_icon="🧠",
    layout="wide"
)

# ---------------- SIDEBAR ----------------
st.sidebar.title("🧠 NoteGen AI")

# Safe image loading (won't crash if image missing)
try:
    st.sidebar.image("assets/logo.png", width=120)
except:
    st.sidebar.info("Logo not found")

st.sidebar.markdown("### AI Lecture Notes Generator")
st.sidebar.markdown("Powered by **LLaMA 3.3 (Groq)**")

# ---------------- MAIN UI ----------------
st.title("📘 NoteGen AI")
st.write("Generate **clean, structured notes** using AI.")

text_input = st.text_area(
    "✍️ Paste your lecture text here:",
    height=250
)

generate_btn = st.button("🚀 Generate Notes")

# ---------------- API SETTINGS ----------------
GROQ_API_KEY = os.getenv("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")  # safer than hardcoding
API_URL = "https://api.groq.com/openai/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

# ---------------- AI FUNCTION ----------------
def generate_notes(text):
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "system",
                "content": "You are an expert note-making assistant."
            },
            {
                "role": "user",
                "content": f"Create clear, structured lecture notes:\n{text}"
            }
        ],
        "temperature": 0.3
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"❌ Error: {response.text}"

# ---------------- BUTTON ACTION ----------------
if generate_btn:
    if not text_input.strip():
        st.warning("⚠️ Please enter lecture text first.")
    else:
        with st.spinner("Generating notes..."):
            notes = generate_notes(text_input)

        st.success("✅ Summary Generated!")
        st.markdown("### 📄 Generated Notes")
        st.write(notes)
