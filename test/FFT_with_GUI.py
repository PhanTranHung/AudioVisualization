import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyaudio
import matplotlib.pyplot as plt

CHUNK = 1024 * 1
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

app = QtGui.QApplication([])
view = pg.GraphicsView()
layout = pg.GraphicsLayout(border=(100, 100, 100))
view.setCentralItem(layout)
view.show()
view.setWindowTitle('Visualization')
view.resize(800, 600)

fft_plot = layout.addPlot(title='Filterbank Output', colspan=3)
fft_plot.setRange(yRange=[-1000, 1000])
fft_plot.disableAutoRange(axis=pg.ViewBox.YAxis)
x_data = np.array(range(1, CHUNK + 1))
mel_curve = pg.PlotCurveItem()
# mel_curve.setData(x=x_data, y=x_data * 0)
fft_plot.addItem(mel_curve)

pa = pyaudio.PyAudio()
stream = pa.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    output=True,
    frames_per_buffer=CHUNK)

print("* recording")

for i in range(10000):
    data = stream.read(CHUNK)

    data16 = np.frombuffer(data, dtype=np.int16)
    fft_wave = np.fft.fft(data16)
    fft_wave = fft_wave[:int(CHUNK/2)]/CHUNK
    fft_wave = np.round(fft_wave)
    # fft_wave[1:] = 2*fft_wave[1:]
    pxx = np.abs(fft_wave)

    fft_freq = np.fft.fftfreq(CHUNK, 1./RATE)
    fft_freq = fft_freq[:int(CHUNK/2)]

    mel_curve.setData(x=fft_freq, y=pxx)
    app.processEvents()
    print(pxx.max())
    # stream.write(data)



print("* stopped")

stream.stop_stream()
stream.close()
pa.terminate()




