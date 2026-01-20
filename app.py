import os
import streamlit as st
import requests

# Read API key from Hugging Face Secrets
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    st.error("❌ GROQ_API_KEY not set! Add it in Settings → Variables & Secrets.")
    st.stop()

# Page setup
st.set_page_config(page_title="🧠 NoteGen AI", page_icon="📝", layout="centered")
st.title("🧠 NoteGen AI")
st.subheader("Generate lecture notes automatically using AI")

# User input
lecture_text = st.text_area("Paste your lecture/text here:", height=250)
summary_length = st.slider("Summary Length (approx):", 50, 500, 200)
generate_button = st.button("Generate Notes")

# Function to call Groq API
def generate_notes(text, max_tokens=200):
    url = "https://api.groq.ai/v1/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3-8b-8192",  # Free Groq model
        "prompt": f"Summarize the following lecture into clear notes:\n{text}\n\nNotes:",
        "max_output_tokens": max_tokens,
        "temperature": 0.3
    }
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data["completions"][0]["text"].strip()
    except Exception as e:
        st.error(f"❌ API Request Failed: {e}")
        return None

# Generate notes
if generate_button:
    if not lecture_text.strip():
        st.warning("⚠ Please enter some text to generate notes.")
    else:
        with st.spinner("Generating notes..."):
            notes = generate_notes(lecture_text, max_tokens=summary_length)
        if notes:
            st.success("✅ Notes Generated Successfully!")
            st.text_area("Generated Notes:", notes, height=300)
            st.download_button("💾 Download Notes", notes, file_name="lecture_notes.txt")
