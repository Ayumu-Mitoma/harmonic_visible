import const as C
import audio_processing as ap
import numpy as np
import streamlit as st
from audio_recorder_streamlit import audio_recorder

"""
wav_io = ap.m4a_to_wav(file)
noise_wav_io = ap.noise_reducer(wav_io, num = 0.8)
cqt = ap.create_CQT(noise_wav_io, C.LOW_TUNING)
row = ap.search_max_index(cqt)
#row_84 = ap.create_12_data(row)
row_84 = ap.create_12_data_beta(row)
ap.display_cqt_value(row_84)
peak = ap.peak_extraction(row_84)
ap.display_cqt_value(peak)
"""

#UI部分記述
st.title("倍音成分を見てみよう！")

st.header("手順通りに進めてみよう")
st.subheader("1. 音を録音しよう")
st.text("ピアノの近くにスマホを置いて録音してみよう")

st.subheader("2. 録音した音声を渡してね")
st.text("ボタンを押して録音した音声を選んでね")

audio_byte = audio_recorder()
if st.button("録音を保存"):
    with open("recorder.wav", "wb") as f:
        f.write(audio_byte)
    st.success("録音が保存できました。")