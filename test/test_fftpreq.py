import numpy as np
import matplotlib.pyplot as plt

#fs is sampling frequency
fs = 100.0
time = np.linspace(0,10,int(10*fs),endpoint=False)

#wave is the sum of sine wave(1Hz) and cosine wave(10 Hz)
wave = np.sin(np.pi*time)+ np.cos(np.pi*time)
#wave = np.exp(2j * np.pi * time )

plt.plot(time, wave)
plt.xlim(0,10)
plt.xlabel("time (second)")
plt.title('Original Signal in Time Domain')

plt.show()

# Compute the one-dimensional discrete Fourier Transform.

fft_wave = np.fft.fft(wave)

# Compute the Discrete Fourier Transform sample frequencies.

fft_fre = np.fft.fftfreq(n=wave.size, d=1/fs)

plt.subplot(211)
plt.plot(fft_fre, fft_wave.real, label="Real part")
plt.legend(loc=1)
plt.title("FFT in Frequency Domain")

plt.subplot(212)
plt.plot(fft_fre, fft_wave.imag,label="Imaginary part")
plt.legend(loc=1)
plt.xlabel("frequency (Hz)")

plt.show()