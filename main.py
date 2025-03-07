import const as C
import audio_processing as ap
import numpy as np
import streamlit as st
from audio_recorder_streamlit import audio_recorder
from io import BytesIO
import time
import pandas as pd
import matplotlib.pyplot as plt

#toneの定義
tone_en = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
tone_ja = ["ド", "ド#", "レ", "レ#", "ミ", "ファ", "ファ#", "ソ", "ソ#", "ラ", "ラ#", "シ"]

def display_cqt_value(data, peak_tone):
    fig, ax = plt.subplots()
    x = range(0,len(data))
    index = []

    for i in range(len(data)):
        if data[i] != 0:
            index.append(i)
    ax.bar(x, data)
    ax.set_xlabel("Overtone")
    ax.set_ylabel("Amplitude")
    ax.set_xticks(index)
    ax.set_xticklabels(peak_tone)
    ax.set_yticks([])
    st.pyplot(fig)

#UI部分記述
st.title("倍音成分を見てみよう！")
st.text("サイドバーから操作を選んでね")
st.text("")
choice = ["今から音を録音する", "録音した音を選ぶ"]
option = st.sidebar.selectbox("次の操作を選んでね",choice)

#録音する際の処理部分
if option == "今から音を録音する":
    #音を録音する際の処理
    st.subheader("1. 音を録音しよう")
    st.text("ピアノの近くにスマホを置いて録音してみよう")
   
    #セッション状態の管理
    st.session_state["analysis"] = False
    st.session_state["result"] = False
    
    #録音部分
    audio_bytes = audio_recorder(
        energy_threshold=(100.0, -1.0),
        neutral_color="#4169e1",
        text="ボタンを押して録音",
        icon_size="3x"
    )
    #録音後の処理
    if audio_bytes:
        with BytesIO(audio_bytes)as f:
            data = ap.byte_to_audio(f)
        noise_wav_io = ap.noise_reducer(data, num = 0.8)

        st.session_state["analysis"] = True

    #分析の開始
    if st.session_state["analysis"] == True:
        tone = st.selectbox("鳴らした音を選んでね",tone_ja)
        tone = tone_en[tone_ja.index(tone)]
        st.text(tone)
        tuning = 0.0
        ana = st.button("分析開始")
        if ana == True:
            with st.spinner("処理中..."):
                cqt = ap.create_CQT(noise_wav_io, tuning)
                row = ap.search_max_index(cqt)
                row_84 = ap.create_12_data_beta(row)
                peak, tone, peak_only = ap.peak_extraction(row_84)
                st.session_state["result"] = True
    if st.session_state["result"] == True:
        df = pd.DataFrame({
            "音階":tone,
            "数値":peak_only
        })
        st.dataframe(df.T)
        display_cqt_value(peak_only, tone)

elif option == "録音した音を選ぶ":
    st.subheader("1. 録音した音声を渡してね")
    st.text("ボタンを押して録音した音声を選んでね")
    st.text("※wav, mp3ファイル限定")

    st.session_state["analysis2"] = False
    st.session_state["result2"] = False

    file = st.file_uploader("ファイルを選択してね")
    if file is not None:
        file_name = file.name.lower()
        if file_name.endswith(".wav") or file_name.endswith(".mp3"):
            data = ap.byte_to_audio(file)
            st.session_state["analysis2"] = True
        else:
            st.error("対応しているファイルはwavまたはmp3だけです")
            st.stop()

    if st.session_state["analysis2"] == True:
        noise_wav_io = ap.noise_reducer(data, num = 0.8)
        tuning = st.slider(label="チューニングを選択 ※0が規定値",
                           min_value=-1.0,
                           max_value=1.0,
                           value=0.0,
                           step=0.1,
                           format="%0.1f")
        ana = st.button("分析開始")
        if ana == True:
            with st.spinner("処理中..."):
                cqt = ap.create_CQT(noise_wav_io, tuning)
                row = ap.search_max_index(cqt)
                row_84 = ap.create_12_data_beta(row)
                peak, tone, peak_only = ap.peak_extraction(row_84)
                st.session_state["result2"] = True
    if st.session_state["result2"] == True:
        df = pd.DataFrame({
            "音階":tone,
            "数値":peak_only
        })
        st.dataframe(df.T)
        display_cqt_value(peak_only, tone)