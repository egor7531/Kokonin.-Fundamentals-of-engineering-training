import RPi.GPIO as GPIO
from time import sleep

dac = [8, 11, 7, 1, 0, 5, 12, 6]
comp = 14
troyka = 13

GPIO.setmode(GPIO.BCM)

GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)

def dec2bin(num):
    return [int(elem) for elem in bin(num)[2:].zfill(8)]

def adc():
    for i in range(256):
        dac_val = dec2bin(i)
        GPIO.output(dac, dac_val)
        sleep(0.01)
        comp_val = GPIO.input(comp)
        if comp_val:
            return i
    return 0

try:
    while True:
        i = adc()
        voltage = i * 3.3 / 255.0
        if i: print("{:.2f}V".format(voltage))

finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()