import socket

# Adresse IP de l'ESP32 et port sur lequel il écoute
esp32_ip = '10.0.0.171'  # Remplacez par l'adresse IP de votre ESP32
#esp32_ip = '192.168.4.1' 
esp32_port = 1234

# Code à envoyer à l'ESP32
code_to_send = """
#from machine import Pin
#import time


# led = Pin(2, Pin.OUT)

# #while True:
# led.value(1)  # Allumer la LED
# time.sleep(1)
# led.value(0)  # Éteindre la LED
# time.sleep(1)
f()

"""

code_to_send2 = """

# Configuration des broches d'entrées (par exemple, GPIO 14 et GPIO 27)
input1 = Pin(1, Pin.IN)
input2 = Pin(22, Pin.IN)

# Configuration de la broche de sortie (par exemple, GPIO 26)
output = Pin(23, Pin.OUT)

# Lire les états des deux broches d'entrée
state1 = input1.value()
state2 = input2.value()
print (f"state1={state1}")
# Effectuer un ET logique (and) entre les deux états
result = state1 ^ state2

# Mettre à jour la broche de sortie en fonction du résultat de l'ET logique
output.value(result)

# Petit délai pour éviter de surcharger la boucle
time.sleep(0.1)

"""

code_to_send3 = """

from machine import Pin
import time

"""

# Connexion au serveur TCP de l'ESP32
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((esp32_ip, esp32_port))

# Envoyer le code
sock.sendall(code_to_send.encode('utf-8'))

# Fermer la connexion
sock.close()

