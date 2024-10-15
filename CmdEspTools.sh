esptool.py --chip esp32 --port /dev/tty.usbserial-57670576921 --baud 460800 write_flash -z 0x1000 /Micro-python/Micro-python/ESP32_GENERIC-20240602-v1.23.0.bin


screen /dev/tty.usbserial-57670576921 115200
