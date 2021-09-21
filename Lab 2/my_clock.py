import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
from time import strftime
import adafruit_rgb_display.st7789 as st7789

from enum import Enum

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

height = disp.height
width = disp.width
image = Image.new("RGB", (width, height))
rotation = 0

cube_dimension = 3

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

b23 = digitalio.DigitalInOut(board.D23)
b24 = digitalio.DigitalInOut(board.D24)
b23.switch_to_input()
b24.switch_to_input()

class state(Enum):
    NORMAL = 0
    POSITIVE = 1
    NEGATIVE = 2

negativePositive = ["#E5021D", "#481131", "#20222F", "#0234A7", "#0397FD"]
normalPositive = ["#FFFFFF", "#D4EBF3", "#89DBF4", "#0397FD"]
normalNegative = ["#FFFFFF", "#FFE303", "#FF6D02", "#E5021D"]

currState = state.NORMAL
moments = []
cubes = []
x_origin = 0
y_origin = 0
oldTime = time.time()
confirm = True

def instantiateClock():
    currState = state.NORMAL
    moments = []
    cubes = []
    x_origin = 0
    y_origin = 0
    oldTime = time.time()
    return

instantiateClock()

def getColor(currPos, totalLength, priorState, stateNow):
    colorArray = []
    if priorState == state.NORMAL:
        if stateNow == state.POSITIVE:
            colorArray = normalPositive
        elif stateNow == state.NEGATIVE:
            colorArray = normalNegative
    elif priorState == state.POSITIVE:
        if stateNow == state.NORMAL:
            colorArray = normalPositive[::-1]
        elif stateNow == state.NEGATIVE:
            colorArray = negativePositive[::-1]
    elif priorState == state.NEGATIVE:
        if stateNow == state.NORMAL:
            colorArray = normalNegative[::-1]
        elif stateNow == state.POSITIVE:
            colorArray = negativePositive
    # print(str(currPos) + " " + str(len(colorArray)) + " " + str(int(currPos/len(colorArray))))
    return colorArray[int((currPos/totalLength) * (len(colorArray)-1))]

while True:
    # Reset once you reach midnight
    if(len(cubes) == 1440):
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        instantiateClock()

    # Check for button register
    if not b23.value:
        print("b23 pressed")
        confirm = False
        # pause program and determine color
        if currState == state.NORMAL:
            currState = state.POSITIVE
        elif currState == state.POSITIVE:
            currState = state.NEGATIVE
        elif currState == state.NEGATIVE:
            currState = state.NORMAL
    if not b24.value:
        print("b24 pressed")
        if(len(moments) == 0):
            moments.append((state.NORMAL, 0))
        if(moments[-1][0] != currState):
            for i in range(moments[-1][1]-1, len(cubes)):
                cubes[i][1] = getColor(i-moments[-1][1], len(cubes)-moments[-1][1], moments[-1][0], currState)
            moments.append((currState, len(cubes)))
        confirm = True
    
    if not confirm:
        # pause colors until we decide the cube
        time.sleep(0.1)
        continue
    
    # Determine color
    if currState == state.NORMAL:
        color = "#ffffff"
    elif currState == state.POSITIVE:
        color = "#0397FD"
    elif currState == state.NEGATIVE:
        color = "#E5021D"

    # Draw cube
    if time.time()-oldTime >= 1:
        oldTime = time.time()
        cubes.append([(x_origin, y_origin, cube_dimension+x_origin, cube_dimension+y_origin), color])
        if not (len(cubes)%40) == 0:
            x_origin += cube_dimension
        else:
            x_origin = 0
            y_origin += cube_dimension

    for cube in cubes:
        draw.rectangle(cube[0], outline = 0, fill = cube[1])

    # Display image.
    disp.image(image, rotation)
    time.sleep(0.1)
