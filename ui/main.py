import streamlit as st
import requests

st.set_page_config(layout="wide")
st.title("Distributed Whisper Inference")

left_column, _, right_column = st.columns([8, 1, 8])


with left_column:
    st.markdown('<div class="left-col">', unsafe_allow_html=True)
    st.header("Run Whisper Inference")

    video_url = st.file_uploader("Video")

    if st.button(
        "Execute"
    ):
        with st.spinner("Executing Inference Task"):
            pass

with right_column:
    st.markdown('<div class="right-col">', unsafe_allow_html=True)
    st.header("Inference Result")
    st.write("Here will show workflow execution results when workflow finished.")
    st.markdown("</div>", unsafe_allow_html=True)
