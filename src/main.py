import RPi.GPIO as GPIO
import time
import json
import spidev

pinOe = 32
pinLatch = 36

def initGpio():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pinOe, GPIO.OUT)
    GPIO.setup(pinLatch, GPIO.OUT)
    GPIO.output(pinOe, GPIO.LOW)
    GPIO.output(pinLatch, GPIO.LOW)

    spiBus = 0
    spiDevice = 1
    spiMode = 0
    spiFrequency = 10000000

    spi = spidev.SpiDev()
    spi.open(spiBus, spiDevice)

    spi.max_speed_hz = spiFrequency
    spi.mode = spiMode
    return spi

def driveBytes(spi, aBytes):
    spi.writebytes2(aBytes)
    GPIO.output(pinLatch, GPIO.HIGH)
    GPIO.output(pinLatch, GPIO.LOW)

def displayLightIndex(spi, idx):
    myBytes = [0 for i in range(32)]
    myBytes[idx >> 3] = 1 << (idx % 8)
    driveBytes(spi, myBytes)

def getIndex(x, y):
    return (y & 0x7) + ((~y >> 3) << 7) + ((15-x) << 3)

def cartesianToBytes(cartesian):
    myBytes = [0 for i in range(32)]
    for y in range(len(cartesian)):
        for x in range(len(cartesian)):
            if (cartesian[y] >> x) & 0x1:
                idx = getIndex(x, y)
                myBytes[idx >> 3] = myBytes[idx >> 3] | (1 << (idx % 8))
    return myBytes

def driveCartesian(spi, cartesian):
    driveBytes(spi, cartesianToBytes(cartesian))

f = open('library.json')
library = json.load(f)
spi = initGpio()
pwm = GPIO.PWM(32, 10000)
pwm.start(10)

while True:
    driveCartesian(spi, library["misc_images"]["smiley"])
    time.sleep(5)
    driveCartesian(spi, library["misc_images"]["cat"])
    time.sleep(3)

while True:
    for y in range(16):
        for x in range(16):
            displayLightIndex(spi, getIndex(x, y))
            time.sleep(0.15)
