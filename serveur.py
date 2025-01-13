import socket
import threading
import psutil
import os
import datetime
import subprocess

# Fonction pour gérer les clients
def handle_client(client_socket, client_address):
    """
    Gère les requêtes du client connecté.
    :param client_socket: La socket du client.
    :param client_address: L'adresse du client.
    """
    print(f"[INFO] Connexion établie avec {client_address}")

    try:
        while True:
            # Réception de la commande envoyée par le client
            data = client_socket.recv(1024).decode("utf-8")
            if not data:
                break

            print(f"[RECEIVED] {client_address} -> {data}")

            # Gérer les différentes commandes
            if data == "CPU_RAM":
                # Récupérer les infos CPU/RAM avec l'heure actuelle
                cpu = psutil.cpu_percent()
                ram = psutil.virtual_memory().percent
                current_time = datetime.datetime.now().strftime("%H:%M:%S")
                response = f"[{current_time}] CPU: {cpu}%, RAM: {ram}%"
                client_socket.send(response.encode("utf-8"))

            elif data.startswith("KILL:"):
                # Extraire le nom du processus à tuer
                process_name = data.split(":")[1]
                response = kill_process_by_name(process_name)
                client_socket.send(response.encode("utf-8"))

            elif data.startswith("COMMAND:"):
                # Exécuter une commande système
                command = data.split(":", 1)[1]
                response = execute_command(command)
                client_socket.send(response.encode("utf-8"))

            elif data == "EXIT":
                # Fin de la session pour ce client
                response = "Déconnexion réussie."
                client_socket.send(response.encode("utf-8"))
                break

            else:
                # Commande non reconnue
                response = "Commande inconnue. Veuillez réessayer."
                client_socket.send(response.encode("utf-8"))

    except Exception as e:
        print(f"[ERROR] Erreur avec le client {client_address}: {e}")
        client_socket.send(f"Erreur interne du serveur : {e}".encode("utf-8"))

    finally:
        print(f"[INFO] Connexion fermée avec {client_address}")
        client_socket.close()

# Fonction pour tuer un processus par son nom
def kill_process_by_name(process_name):
    try:
        killed = False
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == process_name:  # Vérifie si le nom correspond
                proc.kill()  # Tue le processus
                killed = True
        if killed:
            return f"Processus '{process_name}' terminé avec succès."
        else:
            return f"Erreur : Processus '{process_name}' introuvable."
    except Exception as e:
        return f"Erreur lors de la tentative de tuer le processus '{process_name}': {e}"

# Fonction pour exécuter une commande système
def execute_command(command):
    """
    Exécute une commande système et retourne sa sortie.
    :param command: La commande système à exécuter.
    :return: La sortie de la commande ou un message d'erreur.
    """
    try:
        # Exécution de la commande
        result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding="cp850")
        if result.returncode == 0:
            return f"Résultat de la commande:\n{result.stdout.strip()}"
        else:
            return f"Erreur lors de l'exécution de la commande:\n{result.stderr.strip()}"
    except Exception as e:
        return f"Erreur lors de l'exécution de la commande : {e}"


# Fonction principale du serveur
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 5555))
    server.listen(5)
    print("[SERVEUR] En attente de connexions...")

    while True:
        client_socket, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()
        print(f"[ACTIF] Connexions actives : {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()
