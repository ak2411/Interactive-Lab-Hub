import board
import busio
import adafruit_apds9960.apds9960
import time

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_apds9960.apds9960.APDS9960(i2c)

sensor.enable_proximity = True
sensor.enable_color = True
redlight = 0

while True:
	prox = sensor.proximity
	print(sensor.color_data)
	time.sleep(0.2)