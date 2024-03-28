import RPi.GPIO as GPIO
from time import sleep

dac = [8, 11, 7, 1, 0, 5, 12, 6]
comp = 14
troyka = 13

GPIO.setmode(GPIO.BCM)

GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)

def adc():
    inValue = 0
    for i in range(7, -1, -1):
        inValue += 2**i
        GPIO.output(dac, [int(elem) for elem in bin(inValue)[2:].zfill(8)])
        sleep(0.01)
        comp_val = GPIO.input(comp)
        if comp_val == 1:
            inValue -= 2**i
    return inValue

try:
    while True:
        i = adc()

        voltage = i * 3.3 / 255.0
        if i: print("{:.2f}V".format(voltage))

finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()