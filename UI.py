import streamlit as st

st.title("倍音成分可視化装置")
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    st.write(uploaded_file)