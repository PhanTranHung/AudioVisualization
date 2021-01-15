import pyaudio

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
    print(i)
    data = stream.read(CHUNK)
    stream.write(data)



print("* stopped")

stream.stop_stream()
stream.close()
pa.terminate()
