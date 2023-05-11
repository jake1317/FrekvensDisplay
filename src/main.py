import RPi.GPIO as GPIO
import time
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

spi = initGpio()
pwm = GPIO.PWM(32, 10000)
pwm.start(50)
while True:
    for y in range(16):
        for x in range(16):
            displayLightIndex(spi, getIndex(x, y))
            time.sleep(0.05)
