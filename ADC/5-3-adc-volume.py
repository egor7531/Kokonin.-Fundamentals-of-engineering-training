import RPi.GPIO as GPIO
from time import sleep

led = [2, 3, 4, 17, 27, 22, 10, 9]
dac = [8, 11, 7, 1, 0, 5, 12, 6]
comp = 14
troyka = 13

GPIO.setmode(GPIO.BCM)

GPIO.setup(led, GPIO.OUT)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)

def adc1():
    inValue = 0
    for i in range(7, -1, -1):
        inValue += 2**i
        GPIO.output(dac, [int(elem) for elem in bin(inValue)[2:].zfill(8)])
        sleep(0.01)
        comp_val = GPIO.input(comp)
        if comp_val == 1:
            inValue -= 2**i
    return inValue

def adc2():
    for i in range(256):
        GPIO.output(dac,  [int(elem) for elem in bin(i)[2:].zfill(8)])
        sleep(0.01)
        comp_val = GPIO.input(comp)
        if comp_val:
            return i
    return 0

def volume(val):
    val = int(val/255*8)
    arr = [0]*8
    for i in range(val):
        arr[i] = 1
    return arr
    
try:
    while True:
        i = adc1()
        if i:
            GPIO.output(led, volume(i))
            print(int(i/255*8))

finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()