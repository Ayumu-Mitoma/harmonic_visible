import const as C
import audio_processing as ap
import numpy as np

name = "C1"
audio_path = C.AUDIO_PATH+name+".wav"
noise_audio_path = C.SAVE_PATH+"noise_reduce_sample.wav"


ap.noise_reducer(audio_path, num = 0.8)
cqt = ap.create_CQT(noise_audio_path, C.LOW_TUNING)
row = ap.search_max_index(cqt)
#row_84 = ap.create_12_data(row)
row_84 = ap.create_12_data_beta(row)
ap.display_cqt_value(row_84)
peak = ap.peak_extraction(row_84)
ap.display_cqt_value(peak)