import tkinter as tk
import socket
import threading

# Variables globales
client_socket = None

# Fonction pour se connecter au serveur
def connect_to_server():
    global client_socket
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("127.0.0.1", 5555))
        update_status("Connecté au serveur.")
    except Exception as e:
        update_status(f"Erreur de connexion : {e}")

# Fonction pour demander les infos CPU/RAM
def get_system_info():
    if client_socket:
        try:
            client_socket.send("CPU_RAM".encode("utf-8"))
            response = client_socket.recv(1024).decode("utf-8")
            update_status(response)
        except Exception as e:
            update_status(f"Erreur lors de la demande des infos système : {e}")
    else:
        update_status("Erreur : Non connecté au serveur.")

# Fonction pour envoyer une commande système
def execute_command():
    command = entry_command.get()
    if client_socket and command:
        try:
            client_socket.send(f"COMMAND:{command}".encode("utf-8"))
            response = client_socket.recv(4096).decode("utf-8")  # Augmenté à 4096 pour les longues réponses
            update_status(response)
        except Exception as e:
            update_status(f"Erreur lors de l'exécution de la commande : {e}")
    else:
        update_status("Erreur : Veuillez entrer une commande valide ou connecter au serveur.")

# Fonction pour fermer une application
def kill_application():
    process_name = entry_app_name.get()
    if client_socket and process_name:
        try:
            client_socket.send(f"KILL:{process_name}".encode("utf-8"))
            response = client_socket.recv(1024).decode("utf-8")
            update_status(response)
        except Exception as e:
            update_status(f"Erreur lors de la tentative de fermer l'application : {e}")
    else:
        update_status("Erreur : Veuillez entrer un nom d'application ou connecter au serveur.")

# Fonction pour envoyer la commande EXIT
def exit_client():
    if client_socket:
        try:
            client_socket.send("EXIT".encode("utf-8"))
            response = client_socket.recv(1024).decode("utf-8")
            update_status(response)
            client_socket.close()
        except Exception as e:
            update_status(f"Erreur lors de la déconnexion : {e}")
    else:
        update_status("Erreur : Non connecté au serveur.")

# Met à jour la zone de texte de l'IHM
def update_status(message):
    text_box.insert(tk.END, message + "\n")
    text_box.see(tk.END)  # Scroll automatique

# Interface Graphique
root = tk.Tk()
root.title("Client - Surveillance & Contrôle")

# Bouton Connexion
btn_connect = tk.Button(root, text="Connexion", command=connect_to_server)
btn_connect.pack()

# Bouton Surveillance CPU/RAM
btn_monitor = tk.Button(root, text="Surveiller CPU/RAM", command=get_system_info)
btn_monitor.pack()

# Entrée pour exécuter une commande système
label_command = tk.Label(root, text="Commande système à exécuter :")
label_command.pack()

entry_command = tk.Entry(root, width=50)
entry_command.pack()

btn_execute = tk.Button(root, text="Exécuter la commande", command=execute_command)
btn_execute.pack()

# Entrée pour nom du processus à fermer
label_app_name = tk.Label(root, text="Nom du processus à fermer (ex: notepad.exe) :")
label_app_name.pack()

entry_app_name = tk.Entry(root, width=30)
entry_app_name.pack()

btn_kill = tk.Button(root, text="Fermer l'application", command=kill_application)
btn_kill.pack()

# Bouton pour quitter le client
btn_exit = tk.Button(root, text="Déconnexion", command=exit_client)
btn_exit.pack()

# Zone de texte pour afficher les messages
text_box = tk.Text(root, height=15, width=60)
text_box.pack()

# Lancement de l'interface
root.mainloop()
