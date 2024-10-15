import socket

# Adresse IP de l'ESP32 (obtenue après la connexion au Wi-Fi)
esp32_ip = '192.168.1.x'  # Remplacer par l'adresse IP de ton ESP32
port = 80  # Port du serveur sur l'ESP32

# Création du socket client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connexion au serveur ESP32
    client_socket.connect((esp32_ip, port))
    print(f"Connecté à l'ESP32 sur {esp32_ip}:{port}")

    # Envoi d'une commande type "(1A, 1B) AND 1Y"
    command = "[[1A, 1B], 'AND', [1Y]]"
    client_socket.sendall(command.encode('utf-8'))
    print(f"Commande envoyée : {command}")

    # Réception de la réponse du serveur
    response = client_socket.recv(1024).decode('utf-8')
    print(f"Réponse reçue : {response}")

finally:
    # Fermeture du socket
    client_socket.close()
    print("Connexion fermée")
