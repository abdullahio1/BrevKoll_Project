import streamlit as st
import io
import re
import wave
from google import genai
from google.genai import types

MODEL = "gemini-3.5-flash-lite"
TTS_MODEL = "gemini-3.1-flash-tts-preview"

PROMPT = """You help immigrants in Sweden understand letters from Swedish authorities
(Försäkringskassan, Arbetsförmedlingen, Migrationsverket, Skatteverket, CSN, kommunen).

Read the letter and answer in {language}, using short sentences and simple words.
Use exactly these headings (translated into {language}):

## Who sent it
## What it means
## What you need to do
## Deadlines
## Important Swedish words

Rules:
- Never invent dates, amounts or requirements that are not in the letter.
- Keep Swedish words in Swedish and explain them.
- If it is a decision (beslut), say if and by when it can be appealed (överklagas).
"""


def explain_letter(file_bytes, mime_type, text, language):
    """Send the letter to the AI and return the explanation as text."""
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

    parts = []
    if file_bytes:
        parts.append(types.Part.from_bytes(data=file_bytes, mime_type=mime_type))
    if text:
        parts.append(f"Letter text:\n{text}")

    reply = client.models.generate_content(
        model=MODEL,
        contents=parts,
        config=types.GenerateContentConfig(system_instruction=PROMPT.format(language=language)),
    )
    return reply.text

def text_to_speech(text):
    """Turn text into speech and return it as WAV audio."""
    clean = re.sub(r"[#*_`>-]", "", text)
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
    reply = client.models.generate_content(
        model=TTS_MODEL,
        contents=f"Read this slowly and clearly:\n{clean}",
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Kore")
                )
            ),
        ),
    )
    pcm = reply.candidates[0].content.parts[0].inline_data.data

    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(24000)
        wav.writeframes(pcm)
    return buffer.getvalue()
# ---------- Page ----------
st.set_page_config(page_title="BrevKoll", page_icon="✉️")
st.title("✉️ BrevKoll")
st.write("Got a letter you don't understand? Upload it and we explain it in your language.")

language = st.selectbox("Your language", ["English", "Arabic", "Somali", "Tigrinya", "Dari"])

tab_upload, tab_text = st.tabs(["📄 Upload letter", "⌨️ Paste text"])
with tab_upload:
    uploaded = st.file_uploader("PDF or photo of the letter", type=["pdf", "png", "jpg", "jpeg"])
with tab_text:
    text = st.text_area("Paste the Swedish text", height=200)

if st.button("Explain my letter", type="primary"):
    if not uploaded and not text:
        st.warning("Upload a letter or paste text first.")
    else:
        with st.spinner("Reading your letter..."):
            try:
                file_bytes = uploaded.getvalue() if uploaded else None
                mime_type = uploaded.type if uploaded else None
                st.session_state.answer = explain_letter(file_bytes, mime_type, text, language)
                st.session_state.audio = None
                #st.markdown(answer)
            except Exception as e:
                if "429" in str(e):
                    st.warning("Too many requests right now. Wait a minute and try again.")
                else:
                    st.error(f"Something went wrong: {e}")
if st.session_state.get("answer"):
    st.divider()
    st.markdown(st.session_state.answer)

    if st.button("🔊 Listen"):
        with st.spinner("Creating audio..."):
            try:
                st.session_state.audio = text_to_speech(st.session_state.answer)
            except Exception as e:
                st.error(f"Something went wrong: {e}")

    if st.session_state.get("audio"):
        st.audio(st.session_state.audio, format="audio/wav")
st.caption("Automatic explanation – not legal advice. Don't upload letters with real personal data while testing.")