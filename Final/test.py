import RPi.GPIO as GPIO
import time 
GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
# GPIO.output(5, GPIO.LOW)
# pwm = GPIO.PWM(5, 1000)
# pwm.start(0)
# while True:
#     for dc in range(0, 101, 1):
#         pwm.ChangeDutyCycle(dc)
#         time.sleep(0.01)
#     time.sleep(1)
#     for dc in range(100, -1, -1):
#         pwm.ChangeDutyCycle(dc)
#         time.sleep(0.01)
#     time.sleep(1)
while True:
    GPIO.output(5, True)
    time.sleep(0.1)
    print("slept")
    GPIO.output(5, False)
    # time.sleep(0.1)
    GPIO.output(6, True)
    time.sleep(0.1)
    print("slept2")
    GPIO.output(6, False)
    time.sleep(0.1)
