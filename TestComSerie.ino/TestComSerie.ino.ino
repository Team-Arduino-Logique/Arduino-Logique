void setup() {
  // Initialiser la communication série à 9600 bauds
  Serial.begin(9600);
  
  // Attendre que la connexion série soit établie (utile pour certains environnements comme l'IDE Arduino)
  while (!Serial) {
    ; // Attente que la communication série démarre
  }
  
  Serial.println("Prêt à recevoir des commandes...");
}

void loop() {
  // Vérifier si des données sont disponibles sur le port série
  if (Serial.available() > 0) {
    // Lire la commande reçue
    String cmd = Serial.readStringUntil('\n'); // Lire jusqu'à une nouvelle ligne
    
    // Appeler la fonction compilCode avec la commande reçue
    compilCode(cmd);
  }
}

// Fonction exemple pour traiter la commande
void compilCode(String cmd) {
  // Afficher la commande reçue
  Serial.print("Commande reçue : ");
  Serial.println(cmd);

  // Ajouter ici le traitement spécifique de la commande
  if (cmd == "LED_ON") {
    Serial.println("Allumer la LED");
    // Ajouter le code pour allumer une LED
  } else if (cmd == "LED_OFF") {
    Serial.println("Éteindre la LED");
    // Ajouter le code pour éteindre une LED
  } else {
    Serial.println("Commande inconnue");
  }
}
