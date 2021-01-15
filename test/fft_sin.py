import numpy as np
import matplotlib.pyplot as plt

# sampling information
Fs = 44100 # sample rate
T = 1/Fs # sampling period
t = 10 # seconds of sampling
N = Fs*t # total points in signal
# N = 4096

# signal information
freq = 5000 # in hertz, the desired natural frequency
omega = 2*np.pi*freq # angular frequency for sine waves

t_vec = np.arange(N)*T # time vector for plotting
y = 2*np.sin(omega*t_vec)

plt.plot(t_vec,y)
plt.show()

fft_wave = np.fft.fft(y)[:int(N/2)]/N
fft_freq = np.fft.fftfreq(int(N), T)[:int(N/2)]
# f = Fs*np.arange((N/2))/N
plt.plot(fft_freq, np.around(np.abs(fft_wave), 1))
plt.xscale('log')
plt.yscale('log')
plt.show()

Y_k = np.fft.fft(y)[0:int(N/2)]/N # FFT function from numpy
Y_k[1:] = 2*Y_k[1:] # need to take the single-sided spectrum only
Pxx = np.abs(Y_k) # be sure to get rid of imaginary part

f = Fs*np.arange((N/2))/N # frequency vector

# plotting
fig,ax = plt.subplots()
plt.plot(f,Pxx,linewidth=5)
# ax.set_xscale('log')
# ax.set_yscale('log')
plt.ylabel('Amplitude')
plt.xlabel('Frequency [Hz]')
plt.show()