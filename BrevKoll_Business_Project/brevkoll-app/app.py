import requests
import streamlit as st

st.set_page_config(page_title="BrevKoll", page_icon="✉️")

st.title("✉️ BrevKoll")
st.write("Got a letter you don't understand? Upload it and we explain it in your language.")

language = st.selectbox("Your language", ["English", "Arabic", "Somali", "Tigrinya", "Dari"])
uploaded = st.file_uploader("Upload your letter", type=["pdf", "png", "jpg", "jpeg"])

if uploaded:
    st.success(f"Got your file: {uploaded.name}. Explanation will be in {language}.")