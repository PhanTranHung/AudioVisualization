import pyaudio
import numpy as np
import matplotlib.pyplot as plt

CHUNK = 1024 * 1
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

pa = pyaudio.PyAudio()
stream = pa.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    output=True,
    frames_per_buffer=CHUNK)

print("* recording")

for i in range(200):
    data = stream.read(CHUNK)

    data16 = np.frombuffer(data, dtype=np.int16)
    fft_wave = np.fft.fft(data16)
    fft_freq = np.fft.fftfreq(CHUNK, 1./RATE)

    plt.plot(fft_freq, fft_wave.real)
    plt.show()

    stream.write(data)



print("* stopped")

stream.stop_stream()
stream.close()
pa.terminate()
