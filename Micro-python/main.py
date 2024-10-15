from machine import Pin
import time

led = Pin(2, Pin.OUT)

while True:
    led.value(1)  # Allumer la LED
    time.sleep(3)
    led.value(0)  # Éteindre la LED
    time.sleep(1)
