import streamlit as st
from groq import Groq
import tempfile, os, subprocess, json, re

st.title("استخراج النص")
# client = Groq(api_key=st.secrets["GROQ_API_KEY"])
 
def transcribe_audio_file(path):
    with open(path, "rb") as f:
        transcript = client.audio.transcriptions.create(
            model="whisper-large-v3",
            file=(os.path.basename(path), f),
            response_format="text"
        )
    return transcript

# ── رفع ملف ──
st.markdown("###  رفع ملف فيديو أو صوت")
uploaded = st.file_uploader("ارفع فيديو أو ملف صوتي", type=["mp4", "mp3", "wav", "m4a", "ogg", "webm"])
 
if uploaded:
    if uploaded.size / 1024**2 > 25:
        st.error("الملف أكبر من 25 MB!")
    elif st.button("استخرج النص!", key="file_btn"):
        with st.spinner("جاري استخراج النص..."):
            ext = os.path.splitext(uploaded.name)[-1].lower()
            with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
                tmp.write(uploaded.read())
                path = tmp.name
            try:
                transcript = transcribe_audio_file(path)
            finally:
                os.unlink(path)
 
        if not transcript or len(transcript.strip()) < 5:
            st.error("لم يتم استخراج أي نص من الملف!")
        else:
            st.subheader(" النص المستخرج")
            st.write(transcript)
            st.download_button(" تحميل النص", transcript, file_name="transcript.txt")
 
st.markdown("---")
 