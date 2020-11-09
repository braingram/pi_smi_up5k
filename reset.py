import RPi.GPIO as GPIO
import spidev


creset_pin = 27

# setup gpio pins
print("Setting up gpio pins...")
GPIO.setmode(GPIO.BCM)
GPIO.setup(creset_pin, GPIO.OUT, initial=GPIO.HIGH)
GPIO.output(creset_pin, 0)
