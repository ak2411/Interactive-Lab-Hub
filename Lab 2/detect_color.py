import board
import busio
import digitalio

import adafruit_apds9960.apds9960
import time
import adafruit_rgb_display.st7789 as st7789
from PIL import Image, ImageDraw, ImageFont

# #########
import adafruit_apds9960.apds9960
import busio

# #########


from enum import Enum

# ###########
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_apds9960.apds9960.APDS9960(i2c)
sensor.enable_color = True
# ###########

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

draw = ImageDraw.Draw(image)

draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 255))
disp.image(image, rotation)

class color(Enum):
	RED=0
	GREEN=1
	BLUE=2

color = [color.RED, color.GREEN,  color.BLUE]

b23 = digitalio.DigitalInOut(board.D23)
b24 = digitalio.DigitalInOut(board.D24)
b23.switch_to_input()
b24.switch_to_input()

# ############
def detectUser(myColor):
	# Try to detect for 5 seconds
	draw.rectangle((0, 0, width, height), outline=0, fill=myColor)
	disp.image(image, rotation)
	for i in range(5):
		color_data = sensor.color_data
		max_value = max(color_data[:3])
		# print(str(color_data)+" "+str(max_value))
		if (max_value > 4500):
			# print(color[color_data.index(max_value)])
			return color[color_data.index(max_value)]
		elif (color_data.index(max_value) == 0) and max_value > 2900:
			# print(color[color_data.index(max_value)])
			return color[color_data.index(max_value)]
		time.sleep(1)
	return False
# #############


while True:
	if not b23.value:
		print("b23 pressed")
		user = detectUser((0,0,255))
		if not user:
			print("no friends detected")
		else:
			print(user)
	time.sleep(0.2)

