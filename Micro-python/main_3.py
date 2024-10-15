import network
import time
import socket
import _thread

# Fonction pour connecter l'ESP32 au Wi-Fi
def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF) py
    wlan.active(True)
    if not wlan.isconnected():
        print('Connexion au réseau', ssid)
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print('Connecté au réseau. Adresse IP:', wlan.ifconfig()[0])

# Remplacez ces variables par le nom et le mot de passe de votre réseau Wi-Fi
SSID = 'Betelgeuse'
PASSWORD = 'Olpdsbg@D'
 
connect_wifi(SSID, PASSWORD)

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

# Lancement du thread pour exécuter le code en parallèle
_thread.start_new_thread(run_user_code, ())

# Fonction pour configurer un serveur TCP
def start_tcp_server(port=1234):
    global user_code
    addr = socket.getaddrinfo('0.0.0.0', port)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print('Serveur en écoute sur le port', port)

    while True:
        conn, addr = s.accept()
        print('Connexion de', addr)
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

# Démarrer le serveur TCP sur le port 1234
start_tcp_server(1234)



