import const as C
import audio_processing as ap
import numpy as np
import streamlit as st
from audio_recorder_streamlit import audio_recorder
from io import BytesIO
import time

"""
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
option = st.radio("下から次の操作を選んでね",
                  ["今から音を録音する", "録音した音を選ぶ"])


if option == "今から音を録音する":
    #音を録音する際の処理
    st.subheader("1. 音を録音しよう")
    st.text("ピアノの近くにスマホを置いて録音してみよう")
   
    audio_bytes = audio_recorder(
        energy_threshold=(100.0, -1.0),
        text="ボタンを押して録音"
        icon_size="2x"
    )
    if audio_bytes:
        with BytesIO(audio_bytes)as f:
            data = ap.byte_to_audio(f)
        noise_wav_io = ap.noise_reducer(data, num = 0.8)
        cqt = ap.create_CQT(noise_wav_io, C.LOW_TUNING)
        st.text(cqt.shape)

if option == "録音した音を選ぶ":
    st.subheader("1. 録音した音声を渡してね")
    st.text("ボタンを押して録音した音声を選んでね")
    st.text("※wavファイル限定")


