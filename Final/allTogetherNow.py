import board
from adafruit_seesaw import seesaw, rotaryio, digitalio
import pyaudio
import wave
import os
import time

seesaw = seesaw.Seesaw(board.I2C(), addr=0x36)

seesaw_product = (seesaw.get_version() >> 16) & 0xFFFF
print("Found product {}".format(seesaw_product))
if seesaw_product != 4991:
    print("Wrong firmware loaded?  Expected 4991")

seesaw.pin_mode(24, seesaw.INPUT_PULLUP)
button = digitalio.DigitalIO(seesaw, 24)

encoder = rotaryio.IncrementalEncoder(seesaw)
last_position = 0
isPressing = False

form_1 = pyaudio.paInt16 # 16-bit resolution
chans = 1 # 1 channel
samp_rate = 44100 # 44.1kHz sampling rate
chunk = 4096 # 2^12 samples for buffer
dev_index = 2 # device index found by p.get_device_info_by_index(ii)
# wav_output_filename = 'record.wav' # name of .wav file
audio = pyaudio.PyAudio() # create pyaudio instantiation
frames = []
stream = None

playbackCtr = 0
recordings = ["test1.wav", "recording.wav"]

def PlayRecording(direction):
    global playbackCtr
    recordingLen = len(recordings)
    playbackCtr = (playbackCtr+direction)%recordingLen
    os.system('aplay '+recordings[playbackCtr])
    # if direction > 0:
    #     print("next")
    # elif direction < 0:
    #     print("prev")

def StartRecording():
    global stream
    # create pyaudio stream
    stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                        input_device_index = dev_index,input = True, \
                        frames_per_buffer=chunk)
    print("recording")

def StopRecording():
    global stream
    global audio
    stream.stop_stream()
    stream.close()
    audio.terminate()
    print("stopped")
    wavefile = wave.open(time.strftime("%Y%m%d-%H%M%S")+".wav",'wb')
    wavefile.setnchannels(chans)
    wavefile.setsampwidth(audio.get_sample_size(form_1))
    wavefile.setframerate(samp_rate)
    wavefile.writeframes(b''.join(frames))
    wavefile.close()
    audio = pyaudio.PyAudio() # create pyaudio instantiation
    stream = None

while True:
    position = -encoder.position
    if not button.value and not isPressing:
        isPressing = True
        StartRecording()
    elif not button.value and isPressing:
        data = stream.read(chunk)
        frames.append(data)
    elif button.value and isPressing:
        isPressing = False
        StopRecording()
    elif position != last_position:
        PlayRecording(position-last_position)
        last_position = position

