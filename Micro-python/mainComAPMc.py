import network
import socket
import _thread
import time
from machine import Pin

# Global variable to store the user code
user_code = ""

# Fonction qui exécute le code reçu dans une boucle
def run_user_code():
    global user_code
    while True:
        if user_code:
            try:
                exec(user_code)  # Exécuter dynamiquement le code reçu
            except Exception as e:
                print("Erreur dans le code :", e)
            time.sleep(1)  # Intervalle de 1 seconde entre chaque exécution
        else:
            time.sleep(0.1)

# Fonction pour configurer un point d'accès Wi-Fi
def start_access_point(ssid, password):
    ap = network.WLAN(network.AP_IF)  # Configurer en mode AP (Point d'accès)
    ap.active(True)  # Activer le point d'accès
    ap.config(essid=ssid, password=password)  # Définir le SSID et le mot de passe
    while not ap.active():
        pass  # Attendre l'activation
    print('Point d\'accès démarré avec l\'adresse IP:', ap.ifconfig()[0])
    return ap.ifconfig()[0]  # Retourner l'adresse IP de l'ESP32

# Fonction pour configurer un serveur TCP
def start_tcp_server(ip, port=1234):
    global user_code
    addr = (ip, port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(addr)
    s.listen(1)
    print(f'Serveur TCP en écoute sur {ip}:{port}')

    while True:
        conn, addr = s.accept()
        print('Conmnexion de', addr)
        data = conn.recv(1024)  # Taille maximale des données reçues : 1024 octets
        if not data:
            break

        # Convertir les données en chaîne de caractères
        received_code = data.decode('utf-8').strip()
        print("Code reçu :")
        print(received_code)

        # Vérifier si le message reçu est "stop"
        if received_code.lower() == "stop":
            user_code = ""  # Arrêter le code si "stop" est reçu
            print("Exécution du code arrêtée.")
        else:
            user_code = received_code  # Mise à jour du code à exécuter

        conn.close()

# Lancement du thread pour exécuter le code en parallèle
_thread.start_new_thread(run_user_code, ())

# Démarrer le point d'accès Wi-Fi (SSID = "ESP32-AP", mot de passe = "123456789")
ap_ip = start_access_point("ESP32-AP", "123456789")

# Démarrer le serveur TCP sur l'adresse IP du point d'accès
start_tcp_server(ap_ip, 1234)
