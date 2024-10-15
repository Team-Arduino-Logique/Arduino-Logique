from machine import UART
import sys
import time
import _thread

# Configuration du port série UART
uart = UART(0, baudrate=115200, tx=1, rx=3)  # Configurer UART 0 pour le port série

# Flag pour contrôler l'exécution en boucle
run_code = True
user_code = ""

# Fonction pour exécuter le code reçu
def run_user_code():
    global run_code, user_code
    while True:
        if user_code:  # Si du code a été reçu
            try:
                exec(user_code)  # Exécute le code reçu
            except Exception as e:
                print("Erreur dans l'exécution du code :", e)
            time.sleep(1)  # Délai d'une seconde entre les exécutions
        else:
            time.sleep(0.1)  # Délai pour éviter la surcharge du processeur

# Fonction pour lire le port série de manière non bloquante
def read_serial_input():
    global run_code, user_code
    while True:
        if uart.any():  # Vérifie s'il y a des données disponibles sur le port série
            incoming_data = uart.read().decode('utf-8')  # Lit les données reçues et les décode
            if incoming_data.strip().lower() == "stop":
                run_code = False  # Stop le code si la commande "stop" est reçue
                print("Arrêt de l'exécution du code utilisateur.")
            else:
                user_code = incoming_data  # Met à jour le code à exécuter
                print("Code reçu et prêt à être exécuté.")
        time.sleep(0.1)  # Délai pour éviter de saturer le processeur

# Démarrage de l'exécution du code utilisateur dans un thread séparé
_thread.start_new_thread(run_user_code, ())

# Lecture du port série dans le thread principal
read_serial_input()
 