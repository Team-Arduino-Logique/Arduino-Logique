import network
import socket
import time

# Configuration de la connexion Wi-Fi
ssid = "Votre_SSID"  # Nom du réseau Wi-Fi
password = "Votre_Mot_De_Passe"  # Mot de passe du réseau Wi-Fi

# Fonction pour se connecter au Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connexion au réseau...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            time.sleep(1)
    print('Connecté, adresse IP:', wlan.ifconfig()[0])

# Configuration du serveur socket
def start_server():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]  # Serveur sur le port 80
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print('Serveur prêt, en attente de connexions...')

    while True:
        cl, addr = s.accept()  # Accepter une connexion
        print('Client connecté depuis', addr)
        
        # Lecture des données envoyées par le client
        data = cl.recv(1024).decode('utf-8')
        print('Données reçues:', data)

        reponse ="cmd reçue OK"
        # Envoyer une réponse au client
        cl.send(response.encode('utf-8'))
        cl.close()

# Connexion au réseau Wi-Fi et démarrage du serveur
connect_wifi()
start_server()
