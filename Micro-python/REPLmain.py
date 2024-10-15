with open('main.py', 'w') as f:
    f.write('from machine import Pin\n')
    f.write('import time\n')
    f.write('led = Pin(2, Pin.OUT)\n')
    f.write('while True:\n')
    f.write('    led.value(1)\n')
    f.write('    time.sleep(1)\n')
    f.write('    led.value(0)\n')
    f.write('    time.sleep(1)\n')
