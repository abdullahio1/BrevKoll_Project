import requests
import streamlit as st
from google import genai
st.set_page_config(page_title="BrevKoll", page_icon="✉️")

st.title("✉️ BrevKoll")
st.write("Got a letter you don't understand? Upload it and we explain it in your language.")

language = st.selectbox("Your language", ["English", "Arabic", "Somali", "Tigrinya", "Dari"])
uploaded = st.file_uploader("Upload your letter", type=["pdf", "png", "jpg", "jpeg"])

if uploaded:
    st.success(f"Got your file: {uploaded.name}. Explanation will be in {language}.")
    
    st.divider()

if st.button("Test AI connection"):
    try:
        client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
        reply = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=f"Say hello in {language}, one short sentence.",
        )
        st.write(reply.text)
    except Exception as e:
        if "429" in str(e):
            st.warning("Too many requests right now. Wait a minute and try again.")
        else:
            st.error(f"Something went wrong: {e}")