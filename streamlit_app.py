import streamlit as st
import requests
import os 


st.set_page_config(page_title="Text Summarizer", page_icon="📝", layout="wide")
st.title("📝 AI Text Summarizer")
st.markdown("Paste any long text and get a concise AI summary.")

#reads API_URL from environment so Docker/AWS can override it

API_URL = os.getenv("API_URL", "http://localhost:8000") + "/summarize"


text_input = st.text_area("Input Text", height=250,
    placeholder="Paste a long article here (minimum 50 words)...")

col1, col2 = st.columns(2)
max_len = col1.slider("Max Summary Length", 50, 300, 130)
min_len = col2.slider("Min Summary Length", 10, 100, 30)

# catch slider conflict before sending to API

if min_len >= max_len:

    st.warning("⚠️ Min length must be less than Max length. Adjusting automatically.")

    min_len = max(10, max_len - 20)


if st.button("✨ Summarize", type="primary"):
    if not text_input.strip():
        st.warning("⚠️ Please enter some text first.")
    elif len(text_input.split()) < 50:
        st.warning("⚠️ Text too short. Please provide at least 50 words.")
    else:
        with st.spinner("Summarizing... (first run loads model, may take 60s)"):
            try:
                response = requests.post(
                    API_URL,
                    json={"text": text_input, "max_length": max_len, "min_length": min_len},
                    timeout=120  # FIX #6: first model load can take 60-90s

                )
                if response.status_code == 200:
                    st.success("✅ Summary generated!")
                    st.write(response.json()["summary"])
                else:
                    st.error(f"❌ API Error: {response.json().get('detail', 'Unknown error')}")
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to API. Is FastAPI running on port 8000?")
            except requests.exceptions.Timeout:
                st.error("⏱️ Timed out. Model may still be loading — try again in 30s.")
            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")