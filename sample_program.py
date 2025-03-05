import librosa
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import sawtooth
import sounddevice as sd

sr = 44100
T = 5
f = 65.4

t = np.linspace(0,T, int(sr*T), endpoint=False)
y = sawtooth(2*np.pi*f*t)

cqt = librosa.cqt(y, hop_length=512,
                  n_bins=36*7, bins_per_octave=36, fmin=32.7)

M = np.abs(cqt).T
row = M[100]

data = np.zeros(84)
for i in range(84):
    data[i] = row[3*i]+row[3*i+1]+row[3*i+2]
x = range(len(data))
plt.bar(x,data)
plt.show()

tone = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

if len(data) != 84:
    print("ERROR")
    exit()

peak = np.zeros(84)
for i in range(15):
    max_id = np.argmax(data)
    peak[max_id] = data[max_id]

    data[max_id] = 0
    data[max_id-1] = 0

tone_all=[]   
for i in range(7):
    for j in range(len(tone)):
        tone_all.append(tone[j]+str(i+1))

tone_peak = []
for i in range(len(data)):
    if peak[i] != 0:
        tone_peak.append(tone_all[i])

print(tone_peak)