import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyaudio
import matplotlib.pyplot as plt
import wave

# wav_file_path = '../wav/file_example.wav'
# wav_file_path = '../wav/StarWars3.wav'
wav_file_path = '../wav/Solo Dance.wav'
wf = wave.open(wav_file_path, 'rb')

CHUNK = 512
FORMAT = pyaudio.get_format_from_width(wf.getsampwidth())
CHANNELS = wf.getnchannels()
RATE = wf.getframerate()
IGNORE = 0

app = QtGui.QApplication([])
view = pg.GraphicsView()
layout = pg.GraphicsLayout(border=(100, 100, 100))
view.setCentralItem(layout)
view.show()
view.setWindowTitle('Visualization')
view.resize(800, 300)

left_plot = layout.addPlot(title='Left Channel', colspan=3)
left_plot.setRange(yRange=[0, 1000])
left_plot.disableAutoRange(axis=pg.ViewBox.YAxis)

left_line_p = pg.mkPen((255, 0, 0), width=2)
left_line = pg.PlotCurveItem(pen=left_line_p)
left_plot.addItem(left_line)

right_line_p = pg.mkPen((0, 0, 255), width=2)
right_line = pg.PlotCurveItem(pen=right_line_p)
left_plot.addItem(right_line)

fft_freq = np.fft.fftfreq(CHUNK, 1. / RATE)[IGNORE:int(CHUNK / 2)]

def fft(data):
    fft_wave = np.fft.fft(data)
    fft_wave = fft_wave[:int(CHUNK / 2)] / CHUNK
    # fft_wave = np.round(fft_wave)

    # rfft = np.fft.rfft(data)
    # fft_wave[1:] = 2*fft_wave[1:]
    pxx = np.abs(fft_wave)[IGNORE:]

    return pxx


pa = pyaudio.PyAudio()
stream = pa.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    # input=True,
    output=True,
    frames_per_buffer=CHUNK)

print("* Playing")

# read data
data = wf.readframes(CHUNK)
while len(data) > 0:
    bars = 35
    maxValue = 2 ** 16
    data16 = np.frombuffer(data, dtype=np.int16)

    if CHANNELS == 1:
        fft_wave = fft(data16)
        peak = np.max(np.abs(data16)) / maxValue
        left_line.setData(x=fft_freq, y=fft_wave)

        strBar = "#" * int(peak * bars) + '-' * int(bars - peak * bars)
        print("Peak = [%s]" % strBar)
    else:
        dataL = data16[0::2]
        dataR = data16[1::2]

        peakL = np.max(np.abs(dataL)) / maxValue
        peakR = np.max(np.abs(dataR)) / maxValue

        lString = "#" * int(peakL * bars) + '-' * int(bars - peakL * bars)
        rString = "#" * int(peakR * bars) + '-' * int(bars - peakR * bars)
        print("L=[%s]\t\tR=[%s]" % (lString, rString))

        fft_wave_l = fft(dataL)
        fft_wave_r = fft(dataR)

        left_line.setData(x=fft_freq, y=fft_wave_l)
        right_line.setData(x=fft_freq, y=fft_wave_r)

    app.processEvents()
    # print(pxx.max())
    stream.write(data)
    data = wf.readframes(CHUNK)

print("* stopped")

stream.stop_stream()
stream.close()
pa.terminate()
