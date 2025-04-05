// Définition des broches des capteurs et du piézo
const int lightPin1 = A1;  // Capteur 1 pour palonnier gauche/droit
const int lightPin2 = A0;  // Capteur 2 pour palonnier avant/arrière
const int piezoPin = 8;    // Broche du piézo

// Variables de calibration
int reposValue1 = 0;  // Valeur "repos" du capteur 1
int reposValue2 = 0;  // Valeur "repos" du capteur 2
int piedValue1 = 0;   // Valeur "avec pied" du capteur 1
int piedValue2 = 0;   // Valeur "avec pied" du capteur 2

// Variables pour stocker les valeurs mappées des axes
int axis1 = 0;  // Palonnier gauche/droit
int axis2 = 0;  // Palonnier avant/arrière

void setup() {
  Serial.begin(9600);  // Initialiser la communication série
  pinMode(piezoPin, OUTPUT);  // Configurer la broche du piézo comme sortie

  // Phase de calibration
  calibrate();

  // Afficher les valeurs calibrées
  Serial.println("Calibration terminée !");
  Serial.print("Repos capteur 1 : ");
  Serial.println(reposValue1);
  Serial.print("Avec pied capteur 1 : ");
  Serial.println(piedValue1);
  Serial.print("Repos capteur 2 : ");
  Serial.println(reposValue2);
  Serial.print("Avec pied capteur 2 : ");
  Serial.println(piedValue2);
}

void loop() {
  // Lire les valeurs des capteurs
  int lightValue1 = analogRead(lightPin1);
  int lightValue2 = analogRead(lightPin2);

  // Mapper les valeurs en fonction des données calibrées
  axis1 = map(lightValue1, reposValue1, piedValue1, -100, 100);
  axis2 = map(lightValue2, reposValue2, piedValue2, -100, 100);

  // Limiter les valeurs pour éviter les dépassements
  axis1 = constrain(axis1, -100, 100);
  axis2 = constrain(axis2, -100, 100);

  // Afficher les valeurs sur le moniteur série
  Serial.print(axis1);
  Serial.print(",");
  Serial.println(axis2);
  delay(50);  // Petit délai pour éviter de saturer le moniteur
}

// Fonction de calibration
void calibrate() {
  // Calibration "repos" (sans pied)
  Serial.println("Place les capteurs au repos (sans pied).");
  bip(2);  // Bip sonore pour indiquer l'étape
  delay(3000);  // Attendre 3 secondes

  reposValue1 = analogRead(lightPin1);
  reposValue2 = analogRead(lightPin2);

  // Calibration "avec pied"
  Serial.println("Place ton pied devant les capteurs.");
  bip(3);  // Bip sonore pour indiquer la deuxième étape
  delay(3000);  // Attendre 3 secondes

  piedValue1 = analogRead(lightPin1);
  piedValue2 = analogRead(lightPin2);
}

// Fonction pour faire un bip avec le piézo
void bip(int nbBips) {
  for (int i = 0; i < nbBips; i++) {
    digitalWrite(piezoPin, HIGH);
    delay(200);
    digitalWrite(piezoPin, LOW);
    delay(200);
  }
}