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
    spiFrequency = 500000

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

spi = initGpio()
pwm = GPIO.PWM(32, 10000)
pwm.start(50)
while True:
    print("StartSequence")
    for i in range(255):
        displayLightIndex(spi, i)
        time.sleep(0.05)
