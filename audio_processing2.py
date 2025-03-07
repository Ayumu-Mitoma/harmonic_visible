import numpy as np
import librosa
import noisereduce as nr
import const as C
import soundfile as sf
import matplotlib.pyplot as plt
import io

SR = C.SR
tune = [-1.0, -0.9, -0.8, -0.7, -0.6, 
        -0.5, -0.4, -0.3, -0.2, -0.1, 
        0.0, 
        0.1, 0.2, 0.3, 0.4, 0.5, 
        0.6, 0.7, 0.8, 0.9, 1.0]

def byte_to_audio(data):
    y, sr = librosa.load(data, sr=C.SR)
    return y

def noise_reducer(data, num=0.5):
    #data,sr = librosa.load(data_io, sr=SR)
    noise_reduce_data = nr.reduce_noise(y=data, y_noise=data, sr=SR, prop_decrease=num)
    
    return noise_reduce_data

def create_CQT_20(noise_data):
    cqt_all = []
    data_norm = librosa.util.normalize(noise_data)
    for i in range(21):
        tune_n = tune[i]
        cqt = librosa.cqt(y=data_norm, sr=SR, 
                        hop_length=C.HOP_LENGTH, 
                        n_bins=C.NUM_OCTAVE*C.BINS_PER_OCTAVE, 
                        bins_per_octave=C.BINS_PER_OCTAVE,
                        tuning=tune_n,
                        filter_scale=2.0, fmin=32.7)
        M = np.abs(cqt).T

        MAX = len(M)-1
        flat_index = np.argmax(M)
        row_index, col_index = np.unravel_index(flat_index, M.shape)
        sec = int(C.SR / C.HOP_LENGTH) * 2
        if row_index+sec < MAX:
            max_row_after_1sec = M[row_index+sec, :]
        else:
            max_row_after_1sec = M[MAX, :]

        cqt_all.append(max_row_after_1sec)

    return cqt_all

def display_cqt_value(data):
    x = range(0,len(data))
    tone_all = []
    for i in range(C.NUM_OCTAVE):
        for j in range(12):
            tone_all.append(C.tone[j]+str(i+1))

    plt.bar(x, data)
    plt.show()

def peak_extraction(data, num=15):
    if len(data) != 84:
        print("ERROR")
        exit()

    peak = np.zeros(84)
    peak_index = []
    for i in range(num):
        max_id = np.argmax(data)
        peak[max_id] = data[max_id]
    
        data[max_id] = 0
        data[max_id-1] = 0
        data[max_id+1] = 0

    tone_all=[]   
    for i in range(C.NUM_OCTAVE):
        for j in range(len(C.tone)):
            tone_all.append(C.tone[j]+str(i+1))
    
    tone_peak = []
    for i in range(len(data)):
        if peak[i] != 0:
            tone_peak.append(tone_all[i])
            peak_index.append(round(peak[i],2))

    return peak, tone_peak, peak_index

def create_12_data(data):
    bins = int(C.BINS_PER_OCTAVE / 12)
    data_84 = np.zeros(84)
    for i in range(84):
        for j in range(bins):
            data_84[i] = data_84[i] + data[i*bins+j]

    return data_84

def create_12_data_beta(data):
    bins = int(C.BINS_PER_OCTAVE / 12)
    data_a = np.zeros(len(data))
    for i in range(10000):
        p = np.argmax(data)
        if p == len(data)-1:
            p = p - 1
        data_a[p] = data[p]+data[p-1]+data[p+1]

        data[p] = 0
        data[p-1] = 0
        data[p+1] = 0

        if np.max(data) ==0:
            break

    data_84 = np.zeros(84)
    for i in range(84):
        for j in range(bins):
            data_84[i] = data_84[i] + data_a[i*bins+j]

    return data_84

