import streamlit as st
import requests
from pydub import AudioSegment
import io

st.set_page_config(layout="wide")
st.title("Distributed Whisper Inference")

left_column, _, right_column = st.columns([8, 1, 8])


    
if "file_size" not in st.session_state:
    st.session_state.file_size = None
if "file_size_mb" not in st.session_state:
    st.session_state.file_size_mb = None
if "duration_min" not in st.session_state:
    st.session_state.duration_min = None
if "duration_sec" not in st.session_state:
    st.session_state.duration_sec = None


with left_column:
    st.markdown('<div class="left-col">', unsafe_allow_html=True)
    st.header("Run Whisper Inference")

    uploaded_file = st.file_uploader("Audio File", type=["mp3"])

    # 处理上传的文件
    if uploaded_file is not None:
        with st.spinner("Processing audio file..."):
            # 获取文件大小（以字节为单位）
            st.session_state.file_size = uploaded_file.size
            # 将字节转换为兆字节
            st.session_state.file_size_mb = st.session_state.file_size / (1024 * 1024)

            # 读取上传的 MP3 文件
            audio = AudioSegment.from_file(io.BytesIO(uploaded_file.read()), format="mp3")
            
            # 获取音频长度（以毫秒为单位）
            duration_ms = len(audio)
            # 将毫秒转换为分钟和秒
            st.session_state.duration_min = duration_ms // 60000
            st.session_state.duration_sec = (duration_ms % 60000) // 1000


    # 显示文件大小和音频长度
    if st.session_state.file_size is not None:
        # 创建一个可左右拖动的数字输入框，范围从 1 到音频长度的分钟数
        st.write(f"Audio Length: {st.session_state.duration_min} mins {st.session_state.duration_sec} secs.")
        selected_minute = st.slider("Hire GPU Worker", 1, st.session_state.duration_min + 1)

with right_column:
    st.markdown('<div class="right-col">', unsafe_allow_html=True)
    st.header("Inference Result")
    st.write("Here will show workflow execution results when workflow finished.")
    st.markdown("</div>", unsafe_allow_html=True)
