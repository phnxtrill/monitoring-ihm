# Surveillance et Contrôle de PC à Distance

Une application Python permettant de surveiller et de contrôler un ordinateur à distance via une interface graphique. Ce projet utilise **Tkinter** pour l'interface utilisateur, **psutil** pour la surveillance du système, et **sockets** pour la communication réseau entre un client et un serveur.

## Fonctionnalités

- **Surveillance des ressources système :**
  - Affichage en temps réel de l'utilisation du CPU et de la RAM du serveur.
  - Horodatage des relevés pour chaque métrique.
- **Contrôle à distance :**
  - Exécution de commandes système sur le serveur.
  - Possibilité de fermer un processus à distance via son nom.
- **Interface graphique :**
  - Interface simple et intuitive pour surveiller les ressources et envoyer des commandes.
- **Gestion multi-connexion :**
  - Support de plusieurs clients simultanés grâce au multithreading.

## Installation

1. **Clone le dépôt** :

   ```bash
   git clone https://github.com/ton-utilisateur/surveillance-distance.git
   cd surveillance-distance
   
2. **Installe les dépendances** :

    ```bash
    pip install psutil
    
3. **Lance le serveur** :

     ```bash
     python serveur.py
     
4. **Lance le client** :

     ```bash
     python client.py

## Prérequis

- Python 3.8+
- Bibliothèque psutil
- (Optionnel) Machine virtuelle pour tester le client et le serveur sur des machines distinctes.

## Utilisation

1. **Lancer le serveur** : Exécute le fichier serveur.py sur l'ordinateur qui sera contrôlé.
2. **Connecter le client** : Exécute le fichier client.py sur un autre ordinateur (ou sur le même en test), et spécifie l'adresse IP et le port du serveur.
3. **Surveiller les ressources** : Utilise les boutons de l'interface pour afficher les métriques du serveur (CPU, RAM).
4. **Envoyer des commandes** :
   - Redémarrer le serveur.
   - Fermer un processus en précisant son nom.

## Auteur
Projet réalisé dans le cadre de mes études en BUT Informatique.
