import board
from adafruit_seesaw import seesaw, rotaryio, digitalio

seesaw = seesaw.Seesaw(board.I2C(), addr=0x36)

seesaw_product = (seesaw.get_version() >> 16) & 0xFFFF
print("Found product {}".format(seesaw_product))
if seesaw_product != 4991:
    print("Wrong firmware loaded?  Expected 4991")

seesaw.pin_mode(24, seesaw.INPUT_PULLUP)
button = digitalio.DigitalIO(seesaw, 24)

encoder = rotaryio.IncrementalEncoder(seesaw)
last_position = -1
isPressing = False

def PlayRecording(direction):
    if direction > 0:
        print("next")
    elif direction < 0:
        print("prev")

def StartRecording():
    print("recording")

def StopRecording():
    print("stopped")

while True:
    position = -encoder.position
    if not button.value and not isPressing:
        isPressing = True
        StartRecording()
    elif button.value and isPressing:
        isPressing = False
        StopRecording()
    elif position != last_position:
        PlayRecording(position-last_position)
        last_position = position

