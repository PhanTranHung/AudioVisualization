import pyqtgraph as pg
from pyqtgraph.Qt import QtGui
import numpy as np
import pyaudio
from scipy.ndimage.filters import gaussian_filter1d
import wave

INPUT = False

wav_file_path = '../wav/This Dot Song.wav'
# wav_file_path = '../wav/StarWars3.wav'
# wav_file_path = '../wav/Solo Dance.wav'
if not INPUT:
    wf = wave.open(wav_file_path, 'rb')

CHUNK = 1024
FORMAT = pyaudio.paInt16 if INPUT else pyaudio.get_format_from_width(wf.getsampwidth())
CHANNELS = 1 if INPUT else wf.getnchannels()
RATE = 44100 if INPUT else wf.getframerate()
IGNORE_START = 1
IGNORE_END = CHUNK // 3  # = CHUNK/2 * 2/3, take only 2/3

app = QtGui.QApplication([])
view = pg.GraphicsView()
layout = pg.GraphicsLayout(border=(100, 100, 100))
view.setCentralItem(layout)
view.show()
view.setWindowTitle('Visualization')
view.resize(800, 600)

topPlot = layout.addPlot(title='Left Channel', colspan=3)
topPlot.setRange(yRange=[0, 200])
topPlot.disableAutoRange(axis=pg.ViewBox.YAxis)

left_line_p = pg.mkPen((255, 0, 0), width=1)
left_line = pg.PlotCurveItem(pen=left_line_p)
topPlot.addItem(left_line)

right_line_p = pg.mkPen((0, 0, 255), width=1)
right_line = pg.PlotCurveItem(pen=right_line_p)
topPlot.addItem(right_line)

fft_freq = np.fft.rfftfreq(CHUNK, 1. / RATE)[IGNORE_START:IGNORE_END]

hamming_window = np.hamming(CHUNK // 2)


def fft(data):
    fft_wave = np.fft.rfft(data) / CHUNK
    pxx = np.abs(fft_wave)[IGNORE_START:IGNORE_END]
    h_data = hamming_window[IGNORE_START:IGNORE_END] * pxx
    rouned = np.around(h_data)
    fft_data = gaussian_filter1d(rouned, sigma=1.0)
    return fft_data


pa = pyaudio.PyAudio()
stream = pa.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=INPUT,
    output=True,
    frames_per_buffer=CHUNK)

print("* Playing")

# read data
data = stream.read(CHUNK) if INPUT else wf.readframes(CHUNK)
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
    data = stream.read(CHUNK) if INPUT else wf.readframes(CHUNK)

print("* stopped")

stream.stop_stream()
stream.close()
pa.terminate()
